from project_config import MODEL_PATH, video_path, validate_resources

validate_resources()

import cv2
from ultralytics import YOLO
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

# Load YOLOv8 model
model = YOLO(str(MODEL_PATH))  # Replace with your custom model if needed

vehicle_classes = ['car', 'bus', 'truck', 'motorcycle']
directions = {
    'Frame 1': video_path("north"),
    'Frame 2': video_path("east"),
    'Frame 3': video_path("south"),
    'Frame 4': video_path("west")
}

vehicle_counts = {}
time_allocations = {}
resultant_frame = None

def detect_vehicles(video_path):
    global resultant_frame
    cap = cv2.VideoCapture(video_path)
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            raise RuntimeError(f"Cannot read video: {video_path}")
        results = model(frame)
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls)
                label = model.names[cls_id]
                if label in vehicle_classes:
                    count += 1
        resultant_frame = frame  # Save last frame for display
        break  # Analyze only the first frame
    cap.release()
    return count

# Run detection for all directions
for direction, video in directions.items():
    try:
        vehicle_count = detect_vehicles(video)
    except Exception as e:
        raise RuntimeError(f"Detection failed for {video}") from e
    vehicle_counts[direction] = vehicle_count
    time_allocations[direction] = min(8 + vehicle_count, 30)  # Example: 8 + vehicle_count seconds

# Create GUI
window = tk.Tk()
window.title("Result Window")
window.geometry("600x400")

# Display result labels
row = 0
col = 0
for i, (direction, count) in enumerate(vehicle_counts.items()):
    time_alloc = time_allocations[direction]
    frame = tk.Frame(window)
    tk.Label(frame, text=f"Result for {direction}", font=("Helvetica", 12, "bold"), fg="red").pack()
    tk.Label(frame, text=f"Total Number of Vehicles : {count}", font=("Helvetica", 10)).pack()
    tk.Label(frame, text=f"Time Allocated : {time_alloc} seconds", font=("Helvetica", 10)).pack()
    frame.grid(row=row, column=col, padx=20, pady=20)
    col += 1
    if col > 1:
        row += 1
        col = 0

# Show resultant frame
def show_result_frame():
    if resultant_frame is not None:
        img = cv2.cvtColor(resultant_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = img.resize((500, 300))
        img_tk = ImageTk.PhotoImage(img)

        top = tk.Toplevel()
        top.title("Detected Frame")
        label = Label(top, image=img_tk)
        label.image = img_tk
        label.pack()

Button(window, text="Show Resultant Frame", command=show_result_frame).grid(pady=10)

window.mainloop()

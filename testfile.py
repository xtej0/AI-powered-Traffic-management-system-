from project_config import MODEL_PATH, video_path, validate_resources

validate_resources()

import cv2
import numpy as np
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO(str(MODEL_PATH))

# Classes to consider as vehicles
vehicle_classes = ['car', 'truck', 'bus', 'motorcycle', 'ambulance']

# Input video files (Source_vids directory)
directions = {
    "Frame 1": video_path("north"),  # North
    "Frame 2": video_path("east"),  # East
    "Frame 3": video_path("south"),  # South
    "Frame 4": video_path("west"),  # West
}

vehicle_counts = {}
time_allocations = {}
resultant_frames = {}

def detect_vehicles(video_path):
    cap = cv2.VideoCapture(video_path)
    count = 0
    output_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            raise RuntimeError(f"Cannot read video: {video_path}")

        results = model(frame)
        output_frame = frame.copy()

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls)
                label = model.names[cls_id]
                if label in vehicle_classes:
                    count += 1
                    coords = box.xyxy[0].cpu().numpy().astype(int)
                    cv2.rectangle(output_frame, (coords[0], coords[1]), (coords[2], coords[3]), (0, 255, 0), 2)
                    cv2.putText(output_frame, label, (coords[0], coords[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        break  # Only process first frame

    cap.release()
    return count, output_frame

# Process all 4 directions
for frame_key, video_path in directions.items():
    try:
        count, frame = detect_vehicles(video_path)
    except Exception as exc:
        raise RuntimeError(f"Detection failed for {video_path}") from exc

    vehicle_counts[frame_key] = count
    time_allocations[frame_key] = min(8 + count, 30)  # Ensure timing is capped at 30 seconds
    resultant_frames[frame_key] = frame

# Create GUI
window = tk.Tk()
window.title("Traffic Management System")

# Add result labels
row = 0
col = 0
for frame_key in directions.keys():
    frame = tk.Frame(window)
    frame.grid(row=row, column=col, padx=10, pady=10)

    Label(frame, text=f"Result for {frame_key}", fg="red", font=('Arial', 14, 'bold')).pack()
    Label(frame, text=f"Total Number of Vehicles : {vehicle_counts[frame_key]}", font=('Arial', 12)).pack()
    Label(frame, text=f"Time Allocated : {time_allocations[frame_key]} seconds", font=('Arial', 12)).pack()

    col += 1
    if col > 1:
        col = 0
        row += 1

# Function to display result frames
def show_result_frame(frame_key):
    frame = resultant_frames.get(frame_key)
    if frame is not None:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = img.resize((500, 300))
        img_tk = ImageTk.PhotoImage(img)

        top = tk.Toplevel()
        top.title(f"{frame_key} - Result Frame")
        label = Label(top, image=img_tk)
        label.image = img_tk
        label.pack()

# Add buttons to display each frame
button_frame = tk.Frame(window)
button_frame.grid(row=row+1, column=0, columnspan=2, pady=15)

for frame_key in directions.keys():
    Button(button_frame, text=f"Show {frame_key}", command=lambda k=frame_key: show_result_frame(k)).pack(side='left', padx=5)

window.mainloop()

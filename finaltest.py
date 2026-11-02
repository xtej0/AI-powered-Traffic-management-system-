from project_config import MODEL_PATH, video_path, validate_resources

validate_resources()

import cv2
import numpy as np
import tkinter as tk
from tkinter import Label, Button
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO(str(MODEL_PATH))

vehicle_classes = ['car', 'truck', 'bus', 'motorcycle', 'ambulance']

# Video sources (Source_vids directory)
directions = {
    "Frame 1": video_path("north"),  # North
    "Frame 2": video_path("east"),  # East
    "Frame 3": video_path("south"),  # South
    "Frame 4": video_path("west"),  # West
}

vehicle_counts = {}
time_allocations = {}

# Run detection only on 1st frame to calculate count and time
def count_vehicles(video_path):
    cap = cv2.VideoCapture(video_path)
    count = 0

    ret, frame = cap.read()
    if not ret:
        cap.release()
        raise RuntimeError(f"Cannot read video: {video_path}")
    if ret:
        results = model(frame)
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls)
                label = model.names[cls_id]
                if label in vehicle_classes:
                    count += 1
    cap.release()
    return count

# Fill results
for key, path in directions.items():
    try:
        count = count_vehicles(path)
    except Exception as exc:
        raise RuntimeError(f"Detection failed for {path}") from exc
    vehicle_counts[key] = count
    time_allocations[key] = min(8 + count, 30)

# GUI setup
window = tk.Tk()
window.title("Traffic Management System")

row, col = 0, 0
for key in directions.keys():
    frame = tk.Frame(window)
    frame.grid(row=row, column=col, padx=10, pady=10)

    Label(frame, text=f"Result for {key}", fg="red", font=('Arial', 14, 'bold')).pack()
    Label(frame, text=f"Total Number of Vehicles : {vehicle_counts[key]}", font=('Arial', 12)).pack()
    Label(frame, text=f"Time Allocated : {time_allocations[key]} seconds", font=('Arial', 12)).pack()

    col += 1
    if col > 1:
        col = 0
        row += 1

# Show live detection when button is clicked
def show_video_detection(frame_key):
    video_path = directions[frame_key]
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
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
                    coords = box.xyxy[0].cpu().numpy().astype(int)
                    cv2.rectangle(frame, (coords[0], coords[1]), (coords[2], coords[3]), (0, 255, 0), 2)
                    cv2.putText(frame, label, (coords[0], coords[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow(f"{frame_key} Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Buttons for live video
button_frame = tk.Frame(window)
button_frame.grid(row=row+1, column=0, columnspan=2, pady=15)

for frame_key in directions.keys():
    Button(button_frame, text=f"Show {frame_key} Video", command=lambda k=frame_key: show_video_detection(k)).pack(side='left', padx=5)

window.mainloop()

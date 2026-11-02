from project_config import MODEL_PATH, video_path, validate_resources

validate_resources()

import cv2
from ultralytics import YOLO
import time

# Load YOLOv8 model (change to your trained .pt file if needed)
model = YOLO(str(MODEL_PATH))  # Replace with your custom model if you have one

# Define vehicle and emergency vehicle classes (YOLOv8 pretrained COCO only detects these)
vehicle_classes = ['car', 'truck', 'bus', 'motorcycle']
emergency_classes = ['ambulance', 'firetruck']  # Custom model needed to detect these!

# Directions and corresponding video files (update filenames to match your footage)
directions = {
    'North': video_path("north"),
    'East': video_path("east"),
    'South': video_path("south"),
    'West': video_path("west")
}

# Base timing (in seconds)
BASE_GREEN_TIME = 15
EMERGENCY_EXTRA_TIME = 15

print("\n--- Cycle Start ---\n")

# Process each direction
for direction, video_path in directions.items():
    print(f"Processing {direction}...")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Error opening video for {direction}: {video_path}")
        continue

    vehicle_count = 0
    emergency_detected = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLOv8 detection
        results = model(frame)
        annotated_frame = results[0].plot()

        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls)
                cls_name = model.names[cls_id]

                print(f"Detected: {cls_name}")

                if cls_name in vehicle_classes:
                    vehicle_count += 1
                if cls_name.lower() in emergency_classes:
                    emergency_detected = True

        # Show the detection window
        cv2.imshow(f"{direction} Detection", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"🚗 Vehicles detected: {vehicle_count}")
    print(f"🚨 Emergency vehicle detected: {emergency_detected}")

    # Calculate green light time
    if emergency_detected:
        green_time = BASE_GREEN_TIME + EMERGENCY_EXTRA_TIME
    else:
        green_time = BASE_GREEN_TIME + min(vehicle_count * 2, 30)

    print(f"🟢 {direction} GREEN for {green_time} seconds")
    time.sleep(1)  # Simulate green light duration
    print(f"🔴 {direction} RED\n")

print("--- Cycle End ---")

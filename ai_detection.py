from ultralytics import YOLO
import cv2
import math
import time
import os
import requests

# ==============================
# INPUT SOURCE
# ==============================
USE_WEBCAM = True       # False = test.mp4 | True = Webcam
VIDEO_PATH = "test.mp4"
WEBCAM_INDEX = 0
# ==============================

# Create evidence folder
if not os.path.exists("evidence"):
    os.makedirs("evidence")

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open video / webcam
cap = cv2.VideoCapture(WEBCAM_INDEX if USE_WEBCAM else VIDEO_PATH)
if not cap.isOpened():
    print("❌ Cannot open video/webcam")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

WINDOW_NAME = "Smart Surveillance System"
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

# ==============================
# PARAMETERS
# ==============================
restricted_zone = (450, 50, 630, 430)

LOITER_TIME = 10

prev_positions = {}
loiter_start_time = {}

trespass_snapshot_saved = False
weapon_snapshot_saved = False

print("Running with:", "Webcam" if USE_WEBCAM else "test.mp4")
print("Press 'q' to exit")

# ==============================
# MAIN LOOP
# ==============================
while True:
    ret, frame = cap.read()

    if not ret:
        if USE_WEBCAM:
            continue
        else:
            break

    results = model(frame)
    person_id = 0

    # Draw restricted zone
    rx1, ry1, rx2, ry2 = restricted_zone
    cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (255, 0, 0), 2)
    cv2.putText(frame, "RESTRICTED ZONE",
                (rx1, ry1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # ================= PERSON LOGIC =================
            if cls_id == 0:  # Person
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                label = "NORMAL"

                # Loitering logic (present)
                if person_id in prev_positions:
                    px, py = prev_positions[person_id]
                    distance = math.hypot(cx - px, cy - py)

                    if distance < 5:
                        if person_id not in loiter_start_time:
                            loiter_start_time[person_id] = time.time()
                        elif time.time() - loiter_start_time[person_id] > LOITER_TIME:
                            label = "LOITERING"
                    else:
                        loiter_start_time.pop(person_id, None)

                # Trespassing (snapshot on entry)
                if rx1 < cx < rx2 and ry1 < cy < ry2:
                    label = "TRESPASSING"
                    if not trespass_snapshot_saved:
                        filename = f"evidence/TRESPASS_{int(time.time())}.jpg"
                        cv2.imwrite(filename, frame)
                        print(f"📸 Trespass snapshot saved: {filename}")
                        trespass_snapshot_saved = True

                        requests.post(
                            "http://127.0.0.1:5000/alert",
                            json={"camera": "CAM-01", "event": "TRESPASSING"}
                        )

                prev_positions[person_id] = (cx, cy)
                person_id += 1

                color = (255, 0, 255) if label == "TRESPASSING" else (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # ================= DANGEROUS OBJECT =================
            if cls_id == 43:  # Knife
                label = "DANGEROUS OBJECT"
                color = (0, 0, 255)

                if not weapon_snapshot_saved:
                    filename = f"evidence/WEAPON_{int(time.time())}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"🚨 Weapon detected: {filename}")
                    weapon_snapshot_saved = True

                    requests.post(
                        "http://127.0.0.1:5000/alert",
                        json={"camera": "CAM-01", "event": "DANGEROUS OBJECT"}
                    )

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow(WINDOW_NAME, frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Program exited cleanly.")
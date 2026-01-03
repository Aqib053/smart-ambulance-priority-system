import cv2
import time
import os
import requests
from ultralytics import YOLO
from requests.exceptions import RequestException

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "ambulance_best.pt")
BACKEND_URL = "http://127.0.0.1:8000/ambulance/detected"
SIGNAL_ID = "SIG_01"

CONF_THRESHOLD = 0.55
COOLDOWN_SECONDS = 15
CAMERA_INDEX = 0
# ---------------------------------------


# ---------- Model Check ----------
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "\n❌ YOLO model not found.\n"
        "➡ Please download 'ambulance_best.pt'\n"
        "➡ Place it inside: detection/models/\n"
    )

print("✅ YOLO model found. Loading model...")
model = YOLO(MODEL_PATH)


# ---------- Camera Check ----------
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("❌ Camera not available. Please check camera connection.")
    exit(1)

print("📷 Camera initialized successfully")


# ---------- Runtime State ----------
last_trigger_time = 0


# ---------- Main Loop ----------
while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Failed to read frame from camera")
        break

    ambulance_detected = False

    # Run inference
    try:
        results = model(frame, conf=CONF_THRESHOLD, verbose=False)
    except Exception as e:
        print("❌ Model inference failed:", e)
        continue

    # Parse results
    for result in results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            class_id = int(box.cls[0])

            # Class 0 → ambulance (single-class model)
            if class_id == 0:
                ambulance_detected = True

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    "AMBULANCE",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

    # ---------- Trigger Backend ----------
    current_time = time.time()
    if ambulance_detected and (current_time - last_trigger_time) > COOLDOWN_SECONDS:
        try:
            response = requests.post(
                BACKEND_URL,
                json={"signal_id": SIGNAL_ID},
                timeout=3
            )

            if response.status_code == 200:
                print("🚑 Ambulance confirmed → Signal triggered")
                last_trigger_time = current_time
            else:
                print("⚠️ Backend rejected request:", response.text)

        except RequestException as e:
            print("❌ Failed to contact backend:", e)

    # ---------- Display ----------
    cv2.imshow("Smart Ambulance Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("👋 Exiting detection")
        break


# ---------- Cleanup ----------
cap.release()
cv2.destroyAllWindows()

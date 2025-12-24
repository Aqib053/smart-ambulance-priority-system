from ultralytics import YOLO
import cv2
import requests
import time

# ---------------- LOAD CUSTOM MODEL ----------------
model = YOLO("ambulance_best.pt")

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)

# ---------------- BACKEND ----------------
BACKEND_URL = "http://127.0.0.1:8000/ambulance/detected"

# ---------------- CONTROL PARAMETERS ----------------
CONF_THRESHOLD = 0.55          # higher confidence
MIN_BOX_AREA = 25000           # ignore small objects (phones/hands)
ASPECT_MIN = 1.6               # ambulance-like rectangle
ASPECT_MAX = 3.8
DETECTION_TIME = 2.5           # seconds object must stay visible
TRIGGER_COOLDOWN = 20           # seconds between triggers

last_trigger = 0
detection_start = None

print("🚦 Ambulance detection system started")

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_h, frame_w = frame.shape[:2]
    frame_area = frame_h * frame_w

    results = model(frame, conf=CONF_THRESHOLD, verbose=False)

    ambulance_confirmed = False

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            # Only ambulance class
            if cls != 0:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            width = x2 - x1
            height = y2 - y1
            area = width * height

            # ---------------- FILTER 1: SIZE ----------------
            if area < MIN_BOX_AREA:
                continue

            # ---------------- FILTER 2: DISTANCE ----------------
            if area < 0.12 * frame_area:
                continue

            # ---------------- FILTER 3: SHAPE ----------------
            aspect_ratio = width / height
            if not (ASPECT_MIN <= aspect_ratio <= ASPECT_MAX):
                continue

            # ---------------- PASSED ALL FILTERS ----------------
            ambulance_confirmed = True

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"AMBULANCE {conf:.2f}"
            cv2.putText(
                frame, label, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
            )

    # ---------------- TIME-BASED CONFIRMATION ----------------
    if ambulance_confirmed:
        if detection_start is None:
            detection_start = time.time()
        elif time.time() - detection_start >= DETECTION_TIME:
            if time.time() - last_trigger >= TRIGGER_COOLDOWN:
                print("🚑 Confirmed ambulance → Triggering signal")
                try:
                    requests.post(BACKEND_URL, json={"signal_id": "SIG_01"})
                except:
                    print("⚠️ Backend not reachable")

                last_trigger = time.time()
                detection_start = None
    else:
        detection_start = None

    cv2.imshow("Ambulance Detection (Precision Filtered)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

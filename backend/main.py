from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import threading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- SIGNAL STATE ----------------
signal_state = {
    "SIG_01": "RED"
}

# ---------------- HOSPITAL ALERT STATE ----------------
hospital_alert = {
    "status": "IDLE",               # IDLE | INCOMING | ACKNOWLEDGED
    "message": "",
    "eta_seconds": 0,
    "emergency_type": "",
    "severity": "",
    "acknowledged": False
}

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "Backend is running"}

# ---------------- AMBULANCE DETECTED ----------------
@app.post("/ambulance/detected")
def ambulance_detected(data: dict):
    signal_id = data.get("signal_id", "SIG_01")

    print(f"🚑 Ambulance detected at signal: {signal_id}")

    # Trigger signal
    if signal_state[signal_id] != "GREEN":
        trigger_signal(signal_id)

    # Trigger hospital alert
    hospital_alert.update({
        "status": "INCOMING",
        "message": "Incoming ambulance detected. Prepare ER.",
        "eta_seconds": 180,                 # 3 minutes demo ETA
        "emergency_type": "Trauma",
        "severity": "Critical",
        "acknowledged": False
    })

    print("🏥 Hospital alerted")

    return {"status": "signal + hospital alert triggered"}

# ---------------- SIGNAL LOGIC ----------------
def trigger_signal(signal_id):
    print(f"🟢 SIGNAL TURNED GREEN: {signal_id}")
    signal_state[signal_id] = "GREEN"

    def reset():
        time.sleep(10)
        signal_state[signal_id] = "RED"
        print(f"🔴 SIGNAL RESET TO RED: {signal_id}")

    threading.Thread(target=reset).start()

# ---------------- ACKNOWLEDGE FROM HOSPITAL ----------------
@app.post("/hospital/acknowledge")
def acknowledge_alert():
    hospital_alert["acknowledged"] = True
    hospital_alert["status"] = "ACKNOWLEDGED"
    print("✅ Hospital acknowledged alert")
    return {"status": "acknowledged"}

# ---------------- GET STATES ----------------
@app.get("/signal/state")
def get_signal_state():
    return signal_state

@app.get("/hospital/alert")
def get_hospital_alert():
    return hospital_alert

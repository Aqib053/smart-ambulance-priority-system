# 🚑 Smart Ambulance Priority System

## Overview
The Smart Ambulance Priority System is an AI-based prototype designed to reduce ambulance delays at traffic intersections. The system detects an approaching ambulance using computer vision, automatically prioritizes traffic signals, and notifies the destination hospital in real time, enabling faster emergency response.

This project demonstrates how AI, backend services, and simple dashboards can be integrated into a safety-critical workflow.

---

## Problem Statement
Ambulances often lose critical time due to traffic congestion and lack of coordination between traffic systems and hospitals. Even small delays at intersections can significantly impact patient outcomes.

---

## Solution Summary
The system works by:
1. Detecting an ambulance using a camera and a trained YOLO-based model.
2. Sending a real-time alert to a backend service.
3. Automatically switching the traffic signal to green.
4. Notifying the hospital dashboard so staff can prepare in advance.

---

## System Architecture (High-Level)
- AI Detection Module: Camera + YOLO model for ambulance detection  
- Backend Service: FastAPI server for signal control and communication  
- Traffic Signal Logic: Simulated signal state switching  
- Hospital Dashboard: Web-based alert and status display  

---

## Tech Stack
- Language: Python  
- AI / Computer Vision: YOLO (Ultralytics), OpenCV  
- Backend: FastAPI, Uvicorn  
- Frontend: HTML, JavaScript  
- Model Training: Custom ambulance dataset  
- Environment: Python 3.11  

---

## Project Structure
```
smart-ambulance/
├── backend/
│   └── main.py
├── detection/
│   ├── detect_ambulance.py
│   └── models/
│       └── ambulance_best.pt   (download separately)
├── frontend/
│   └── hospital_dashboard.html
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Setup Instructions

### Prerequisites
- Python 3.11
- Webcam (for detection demo)

---

### Create Virtual Environment
```
python3.11 -m venv .venv
source .venv/bin/activate
```

---

### Install Dependencies
```
pip install -r requirements.txt
```

---

### Add Trained Model
Download the trained YOLO model and place it here:
```
detection/models/ambulance_best.pt
```

Note: Model files are intentionally not committed to GitHub.

---

## Running the Project

### Start Backend Server
```
cd backend
uvicorn main:app --reload
```

Backend runs at:
```
http://127.0.0.1:8000
```

---

### Start Ambulance Detection
In a new terminal:
```
cd smart-ambulance
source .venv/bin/activate
python detection/detect_ambulance.py
```

---

### Open Hospital Dashboard
Open the following file in a browser:
```
frontend/hospital_dashboard.html
```

---

## Demo Workflow
1. Camera detects an ambulance.
2. Backend receives detection alert.
3. Traffic signal switches to green.
4. Hospital dashboard receives notification.

---

## Error Handling & Reliability Improvements
- Explicit YOLO model existence checks to prevent crashes  
- Camera availability validation  
- Backend request validation using Pydantic  
- Graceful handling of backend unavailability  
- Relative paths for improved portability  

---

## Known Limitations
- Camera-based detection may fail under occlusion or poor visibility.
- Current implementation supports a single signal for demonstration.
- Traffic signal control is simulated and not hardware-integrated.

---

## Future Enhancements
- Multi-signal green corridor routing
- GPS and siren-based ambulance verification
- Enhanced hospital dashboard with ETA and acknowledgements
- Edge deployment using Jetson Nano or Raspberry Pi
- Integration with real traffic signal controllers

---

## Learning Outcomes
- Understanding the difference between a prototype and a production-ready system
- Importance of validation, error handling, and portability
- Practical experience in end-to-end AI system integration

---

## Acknowledgements
Guidance and mentor feedback played a key role in improving system reliability, structure, and engineering practices.


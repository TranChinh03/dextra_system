
# 🚦 Traffic Detection System

This project implements an **automated traffic flow analysis system** that continuously processes data from 600 cameras every 30 minutes. It uses **YOLO detection** to extract vehicle counts and stores the data in a **Neon database** with auto-partitioning for efficient storage.

---

## 📁 Project Structure

```
traffic-detection-system/
├── detection_service/       # Runs YOLO detections at 00:00, 00:30, ...
├── worker_service/          # Consumes detection results and inserts into NeonDB
├── systemd/                 # Systemd unit files for running as background services
├── README.md                # Project documentation
└── .gitignore
```

---

## ⚙️ Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/traffic-detection-system.git
cd traffic-detection-system
```

### 2️⃣ Create virtual environments
```bash
# For detection service
python3 -m venv venv_detection
source venv_detection/bin/activate
pip install -r detection_service/requirements.txt
deactivate

# For worker service
python3 -m venv venv_worker
source venv_worker/bin/activate
pip install -r worker_service/requirements.txt
deactivate
```

### 3️⃣ Configure Neon database access
Update `worker_service/worker.py` with your Neon database **host, database, username, password**.

---

## 🚀 Running the Services

### 🔹 Using systemd

1. Copy the unit files:
```bash
sudo cp systemd/detection.service /etc/systemd/system/detection.service
sudo cp systemd/worker.service /etc/systemd/system/worker.service
```

2. Reload systemd and enable services:
```bash
sudo systemctl daemon-reload
sudo systemctl enable detection
sudo systemctl enable worker
```

3. Start the services:
```bash
sudo systemctl start detection
sudo systemctl start worker
```

### 🔹 Manual execution (if needed)
```bash
# Detection service
cd detection_service
source ../venv_detection/bin/activate
python run_detection.py

# Worker service
cd worker_service
source ../venv_worker/bin/activate
python worker.py
```

---

## 🔧 Key Features

✅ YOLO detections run **exactly** at the half-hour marks (00:00, 00:30, etc.)  
✅ Data pushed to RabbitMQ and consumed by a worker service  
✅ Worker auto-creates daily partition tables in NeonDB  
✅ Fully managed as background services using systemd for reliability

---

## 📊 Example Detection Entry
```json
{
  "detectionId": "uuid",
  "cameraId": "camera_1",
  "date": "2025-06-06",
  "time": "12:00:00",
  "numberOfBicycle": 2,
  "numberOfMotorcycle": 3,
  "numberOfCar": 5,
  "numberOfVan": 1,
  "numberOfTruck": 0,
  "numberOfBus": 1,
  "numberOfFireTruck": 0,
  "numberOfContainer": 0
}
```

---

## 💡 Notes
- **RabbitMQ** must be running locally (`localhost`) with the `detections` queue.  
- Update `worker_service/worker.py` to match your actual NeonDB credentials.  
- Replace mock detection logic in `detection_service/run_detection.py` with real YOLO inference.  

Enjoy your robust traffic detection system! 🚀

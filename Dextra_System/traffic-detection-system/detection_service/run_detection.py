
import time
from datetime import datetime, timedelta
from uuid import uuid4
import json
import pika
import random

def run_yolo_detection(camera_id):
    return {
        "detectionId": str(uuid4()),
        "cameraId": camera_id,
        "date": datetime.utcnow().strftime('%Y-%m-%d'),
        "time": datetime.utcnow().strftime('%H:%M:%S'),
        "numberOfBicycle": random.randint(0, 50),
        "numberOfMotorcycle": random.randint(0, 80),
        "numberOfCar": random.randint(0, 40),
        "numberOfVan": random.randint(0, 10),
        "numberOfTruck": random.randint(0, 20),
        "numberOfBus": random.randint(0, 5),
        "numberOfFireTruck": random.randint(0, 2),
        "numberOfContainer": random.randint(0, 2)
    }

def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="detections", durable=True)
    return channel, connection

def sleep_until_next_half_hour():
    now = datetime.utcnow()
    next_minute = 30 if now.minute < 30 else 60
    next_half_hour = now.replace(minute=next_minute, second=0, microsecond=0)
    if next_minute == 60:
        next_half_hour += timedelta(hours=1)
        next_half_hour = next_half_hour.replace(minute=0)
    sleep_seconds = (next_half_hour - now).total_seconds()
    print(f"[{datetime.utcnow()}] Sleeping for {sleep_seconds/60:.2f} minutes until next half-hour mark...")
    time.sleep(sleep_seconds)

def main():
    camera_ids = [f"camera_{i}" for i in range(1, 601)]
    while True:
        sleep_until_next_half_hour()
        print(f"[{datetime.utcnow()}] Starting YOLO detections for all cameras.")
        channel, connection = get_rabbitmq_channel()
        for camera_id in camera_ids:
            result = run_yolo_detection(camera_id)
            message = json.dumps(result)
            channel.basic_publish(exchange="", routing_key="detections", body=message,
                                  properties=pika.BasicProperties(delivery_mode=2))
            print(f"[{datetime.utcnow()}] Published detection for {camera_id}")
        connection.close()
        print(f"[{datetime.utcnow()}] Completed this batch of detections.")

if __name__ == "__main__":
    main()

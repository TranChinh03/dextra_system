
import json
import pika
import psycopg2
from datetime import datetime

def callback(ch, method, properties, body):
    detection = json.loads(body)
    conn = psycopg2.connect(
        host="your-neon-host",
        dbname="your-db",
        user="your-user",
        password="your-password",
        port=5432
    )
    cur = conn.cursor()
    table_name = f"detections_{detection['date'].replace('-', '')}"
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            detectionId TEXT PRIMARY KEY,
            cameraId TEXT,
            date DATE,
            time TIME,
            numberOfBicycle INT,
            numberOfMotorcycle INT,
            numberOfCar INT,
            numberOfVan INT,
            numberOfTruck INT,
            numberOfBus INT,
            numberOfFireTruck INT,
            numberOfContainer INT
        );
    """)
    cur.execute(f"""
        INSERT INTO {table_name} (
            detectionId, cameraId, date, time,
            numberOfBicycle, numberOfMotorcycle, numberOfCar,
            numberOfVan, numberOfTruck, numberOfBus,
            numberOfFireTruck, numberOfContainer
        ) VALUES (
            %(detectionId)s, %(cameraId)s, %(date)s, %(time)s,
            %(numberOfBicycle)s, %(numberOfMotorcycle)s, %(numberOfCar)s,
            %(numberOfVan)s, %(numberOfTruck)s, %(numberOfBus)s,
            %(numberOfFireTruck)s, %(numberOfContainer)s
        ) ON CONFLICT (detectionId) DO NOTHING;
    """, detection)
    conn.commit()
    cur.close()
    conn.close()
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Inserted detection from camera {detection['cameraId']} into {table_name}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="detections", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="detections", on_message_callback=callback)
    print("Waiting for detections...")
    channel.start_consuming()

if __name__ == "__main__":
    main()

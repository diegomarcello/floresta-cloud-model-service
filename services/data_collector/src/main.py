from floresta_shared.messaging import MessageBroker
from floresta_shared.database import DatabaseManager
import time
import sys
import os
import datetime

broker = None
db = None

def process_task(message):
    global broker, db
    task_type = message.get("type")
    payload = message.get("payload")
    
    print(f"[DataCollector] Processing {task_type} with payload: {payload}")
    
    if task_type == "START_COLLECTION":
        # Simulate work
        limit = os.getenv("BATCH_LIMIT", "100")
        print(f"[DataCollector] Starting collection (Limit: {limit})...")
        time.sleep(2)
        
        # Save dummy data to Mongo
        try:
            record = {
                "source": payload.get("source", "unknown"),
                "timestamp": datetime.datetime.utcnow(),
                "data": "simulated_data_blob",
                "rows": int(limit)
            }
            db.insert_one("raw_data", record)
            print("[DataCollector] Data saved to MongoDB.")
        except Exception as e:
            print(f"[DataCollector] Failed to save data: {e}")
            
        print("[DataCollector] Collection finished.")
        
        # Notify Master
        if broker:
            broker.publish_task("master", "TASK_COMPLETED", {"service": "data_collector", "status": "success", "rows": 100})

def main():
    global broker, db
    print("[DataCollector] Starting Service...")
    time.sleep(5) # Wait for Redis/Mongo
    
    try:
        # Connect to DB
        db = DatabaseManager()
        db.connect()

        # Connect to Broker
        broker = MessageBroker("data_collector")
        broker.start_consuming(process_task)
    except Exception as e:
        print(f"[DataCollector] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

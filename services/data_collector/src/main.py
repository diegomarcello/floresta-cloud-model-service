from floresta_shared.messaging import MessageBroker
import time
import sys

broker = None

def process_task(message):
    global broker
    task_type = message.get("type")
    payload = message.get("payload")
    
    print(f"[DataCollector] Processing {task_type} with payload: {payload}")
    
    if task_type == "START_COLLECTION":
        # Simulate work
        print("[DataCollector] Starting collection...")
        time.sleep(2)
        print("[DataCollector] Collection finished.")
        
        # Notify Master
        if broker:
            broker.publish_task("master", "TASK_COMPLETED", {"service": "data_collector", "status": "success", "rows": 100})

def main():
    global broker
    print("[DataCollector] Starting Service...")
    time.sleep(5) # Wait for Redis
    
    try:
        broker = MessageBroker("data_collector")
        broker.start_consuming(process_task)
    except Exception as e:
        print(f"[DataCollector] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

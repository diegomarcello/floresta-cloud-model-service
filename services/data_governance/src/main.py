from floresta_shared.messaging import MessageBroker
import time
import sys

broker = None

def process_task(message):
    global broker
    task_type = message.get("type")
    payload = message.get("payload")
    
    print(f"[DataGovernance] Processing {task_type} with payload: {payload}")
    
    if task_type == "VALIDATE_SCHEMA":
        # Simulate Validation
        print("[DataGovernance] Validating data against schema...")
        time.sleep(1)
        print("[DataGovernance] Validation passed.")
        
        # Notify Master
        if broker:
            broker.publish_task("master", "TASK_COMPLETED", {"service": "data_governance", "status": "valid", "issues": []})

def main():
    global broker
    print("[DataGovernance] Starting Service...")
    time.sleep(5) 
    
    try:
        broker = MessageBroker("data_governance")
        broker.start_consuming(process_task)
    except Exception as e:
        print(f"[DataGovernance] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

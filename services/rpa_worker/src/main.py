from floresta_shared.messaging import MessageBroker
import time
import sys

broker = None

def process_task(message):
    global broker
    task_type = message.get("type")
    payload = message.get("payload")
    
    print(f"[RPAWorker] Processing {task_type} with payload: {payload}")
    
    if task_type == "RUN_SCRIPT":
        # Simulate RPA
        print("[RPAWorker] Running automation script...")
        time.sleep(3)
        print("[RPAWorker] Script execution finished.")
        
        # Notify Master
        if broker:
            broker.publish_task("master", "TASK_COMPLETED", {"service": "rpa_worker", "status": "success", "output": "file_generated.pdf"})

def main():
    global broker
    print("[RPAWorker] Starting Service...")
    time.sleep(5) 
    
    try:
        broker = MessageBroker("rpa_worker")
        broker.start_consuming(process_task)
    except Exception as e:
        print(f"[RPAWorker] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

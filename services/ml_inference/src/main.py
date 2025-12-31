from floresta_shared.messaging import MessageBroker
import time
import sys

broker = None

def process_task(message):
    global broker
    task_type = message.get("type")
    payload = message.get("payload")
    
    print(f"[MLInference] Processing {task_type} with payload: {payload}")
    
    if task_type == "PREDICT":
        # Simulate ML prediction
        print("[MLInference] Loading model and predicting...")
        time.sleep(1)
        print("[MLInference] Prediction done.")
        
        # Notify Master
        if broker:
            broker.publish_task("master", "TASK_COMPLETED", {"service": "ml_inference", "status": "success", "prediction": [0.9, 0.1]})

def main():
    global broker
    print("[MLInference] Starting Service...")
    time.sleep(5) 
    
    try:
        broker = MessageBroker("ml_inference")
        broker.start_consuming(process_task)
    except Exception as e:
        print(f"[MLInference] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

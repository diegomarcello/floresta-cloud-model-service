from floresta_shared.messaging import MessageBroker
import time
import sys

broker = None

def process_task(message):
    global broker
    task_type = message.get("type")
    payload = message.get("payload")
    
    print(f"[LLMTuner] Processing {task_type} with payload: {payload}")
    
    if task_type == "FINE_TUNE":
        # Simulate LLM Fine-tuning
        print("[LLMTuner] Starting Fine-tuning process (this takes long)...")
        time.sleep(5)
        print("[LLMTuner] Fine-tuning complete.")
        
        # Notify Master
        if broker:
            broker.publish_task("master", "TASK_COMPLETED", {"service": "llm_tuner", "status": "success", "model_version": "v2"})

def main():
    global broker
    print("[LLMTuner] Starting Service...")
    time.sleep(5) 
    
    try:
        broker = MessageBroker("llm_tuner")
        broker.start_consuming(process_task)
    except Exception as e:
        print(f"[LLMTuner] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

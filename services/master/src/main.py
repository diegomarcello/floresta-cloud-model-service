import time
import sys
from floresta_shared.messaging import MessageBroker

def handle_incoming_updates(message):
    """Handle status updates from workers"""
    source = message.get('source')
    msg_type = message.get('type')
    payload = message.get('payload')
    print(f"[Master] Received update from {source}: {msg_type} | Payload: {payload}")

def run_orchestrator():
    print("[Master] Initializing Orchestrator...")
    # Wait for Redis to be ready
    time.sleep(5)
    
    try:
        broker = MessageBroker("master")
        
        # Start listening in background
        broker.start_consuming_thread(handle_incoming_updates)

        print("[Master] Orchestrator Service Started and Listening.")
        
        # Example Workflow Loop
        while True:
            # Simulate triggering a data collection job
            print("[Master] Triggering Data Collection...")
            broker.publish_task("data_collector", "START_COLLECTION", {"source": "api_v1", "limit": 100})
            
            # Simulate triggering an ML Inference
            time.sleep(5)
            print("[Master] Triggering ML Inference...")
            broker.publish_task("ml_inference", "PREDICT", {"model_id": "churn_v1", "input_data": [1, 2, 3]})
            
            # Simulate triggering RPA
            time.sleep(5)
            print("[Master] Triggering RPA Task...")
            broker.publish_task("rpa_worker", "RUN_SCRIPT", {"script": "invoice_processing", "parameters": {}})

            # Simulate triggering Data Governance
            time.sleep(5)
            print("[Master] Triggering Data Governance Check...")
            broker.publish_task("data_governance", "VALIDATE_SCHEMA", {"dataset": "users", "schema": "v1"})
            
            print("[Master] Cycle complete. Waiting...")
            time.sleep(20)
            
    except Exception as e:
        print(f"[Master] Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_orchestrator()

from floresta_shared.messaging import MessageBroker
import time
import sys

# Monitor is slightly different, it might listen to everything or just heartbeat
# For this example, it acts like a passive logger or heartbeat checker

def main():
    print("[Monitor] Starting Service...")
    time.sleep(5) 
    
    try:
        broker = MessageBroker("monitor")
        
        print("[Monitor] Monitoring system health...")
        while True:
            # In a real app, this would check Redis queue lengths, container stats, etc.
            # Here we just log a heartbeat
            print("[Monitor] System OK. Checking queues...")
            time.sleep(10)
            
    except Exception as e:
        print(f"[Monitor] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

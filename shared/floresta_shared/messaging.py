import redis
import json
import os
import time
import threading
from typing import Dict, Any, Callable

class MessageBroker:
    def __init__(self, service_name: str):
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", 6379))
        self.client = redis.Redis(host=self.redis_host, port=self.redis_port, db=0)
        self.service_name = service_name
        self.pubsub = self.client.pubsub()
        self.running = True

    def publish_task(self, target_service: str, task_type: str, payload: Dict[str, Any]):
        """Send a task to a specific service queue"""
        message = {
            "source": self.service_name,
            "type": task_type,
            "payload": payload,
            "timestamp": time.time()
        }
        channel = f"service:{target_service}"
        self.client.publish(channel, json.dumps(message))
        print(f"[{self.service_name}] Published {task_type} to {channel}")

    def subscribe(self, callback: Callable[[Dict], None]):
        """Listen for messages directed to this service"""
        channel = f"service:{self.service_name}"
        self.pubsub.subscribe(channel)
        print(f"[{self.service_name}] Listening on {channel}...")
        
        # Use a separate thread to handle messages so it doesn't block if needed, 
        # but for simplicity in this loop we can just iterate.
        # However, to allow the main program to do other things, we often run this in a loop
        
        try:
            for message in self.pubsub.listen():
                if not self.running:
                    break
                
                if message['type'] == 'message':
                    data = json.loads(message['data'])
                    try:
                        callback(data)
                    except Exception as e:
                        print(f"[{self.service_name}] Error processing message: {e}")
        except Exception as e:
            print(f"[{self.service_name}] Connection lost or error: {e}")

    def start_consuming(self, callback: Callable[[Dict], None]):
        """Starts consuming in a blocking manner (useful for worker nodes)"""
        self.subscribe(callback)

    def start_consuming_thread(self, callback: Callable[[Dict], None]):
        """Starts consuming in a background thread (useful for master/orchestrator)"""
        t = threading.Thread(target=self.subscribe, args=(callback,))
        t.daemon = True
        t.start()
        return t

    def stop(self):
        self.running = False
        self.pubsub.unsubscribe()
        self.client.close()

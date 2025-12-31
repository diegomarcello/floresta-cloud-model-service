import os
from pymongo import MongoClient
from typing import Optional, Any, Dict, List

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance

    def connect(self):
        if self.client:
            return

        host = os.getenv("MONGO_HOST", "localhost")
        port = int(os.getenv("MONGO_PORT", 27017))
        user = os.getenv("MONGO_USER", None)
        password = os.getenv("MONGO_PASSWORD", None)
        db_name = os.getenv("MONGO_DB", "floresta_db")

        if user and password:
            uri = f"mongodb://{user}:{password}@{host}:{port}/?authSource=admin"
        else:
            uri = f"mongodb://{host}:{port}/"

        print(f"[Database] Connecting to {host}:{port}...")
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Force connection check
            self.client.server_info()
            self.db = self.client[db_name]
            print(f"[Database] Connected to {db_name}")
        except Exception as e:
            print(f"[Database] Connection failed: {e}")
            raise

    def get_collection(self, name: str):
        if not self.db:
            self.connect()
        return self.db[name]

    def insert_one(self, collection: str, document: Dict[str, Any]):
        col = self.get_collection(collection)
        return col.insert_one(document)

    def find(self, collection: str, query: Dict[str, Any] = {}, limit: int = 100) -> List[Dict]:
        col = self.get_collection(collection)
        cursor = col.find(query).limit(limit)
        return list(cursor)

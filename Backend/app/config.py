from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from fastapi import HTTPException

uri = "mongodb+srv://<username>:<password>@python.vq682u3.mongodb.net/?retryWrites=true&w=majority&appName=Python"

client = None
db = None
collection = None
attendance_collection = None
is_connected = False

def check_connection():
    if not is_connected:
        raise HTTPException(status_code=503, detail="MongoDB not connected")

try:
    client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=3000)
    client.admin.command('ping')
    print("MongoDB connected successfully!")
    db = client.emp
    collection = db["employees"]
    attendance_collection = db["attendance"]
    is_connected = True

except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print("MongoDB connection failed:", e)
    is_connected = False
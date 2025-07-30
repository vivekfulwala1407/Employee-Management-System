from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://vivek:vivek123@python.vq682u3.mongodb.net/?retryWrites=true&w=majority&appName=Python"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client.emp

collection = db["employees"]
attendance_collection = db["attendance"]


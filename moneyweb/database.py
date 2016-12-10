from pymongo import MongoClient
from config import MONGO_URL


client = MongoClient(MONGO_URL)

# Specify the database
db = client.get_default_database()
graph_collection = db.graph

import os

envget = os.environ.get

MONGO_URL = envget('MONGODB_URI', 'mongodb://localhost:27017/moneyweb')

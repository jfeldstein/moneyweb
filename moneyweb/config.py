import os

envget = os.environ.get

MONGO_URL = envget('MONGOHQ_URL', 'mongodb://localhost:27017/')

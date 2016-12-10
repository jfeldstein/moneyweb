import os
from flask import Flask, render_template, request, redirect
import pymongo
from pymongo import MongoClient


MONGO_URL = os.environ.get('MONGOHQ_URL')
client = MongoClient(MONGO_URL)

# Specify the database
db = client.app29843323
collection = db.shoutouts

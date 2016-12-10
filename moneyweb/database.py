import os
from flask import Flask, render_template, request, redirect
import pymongo
from pymongo import MongoClient
from config import MONGO_URL


client = MongoClient(MONGO_URL)

# Specify the database
db = client.moneyweb
graph_collection = db.graph

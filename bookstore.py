from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

app = FastAPI()

# Initialize MongoDB client
uri = "mongodb://localhost:27017"
client = AsyncIOMotorClient(uri)

db = client["store"]
collection = db["books"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Book Model
# currently, all fields are required
class Book(BaseModel):
    id: int  # not sure if this one is needed
    title: str
    author: str
    description: str
    price: float
    stock: int

from fastapi import FastAPI, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from typing import List

from models import Book, BookUpdate

app = FastAPI()

# Initialize MongoDB client and Send a ping to confirm a successful connection
uri = "mongodb://localhost:27017"
client = AsyncIOMotorClient(uri)
db = client["bookstore"]
collection = db["books"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Adds a new book to the store
@app.post("/books", response_description="Add a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
async def add_new_book(request: Request, book: Book = Body(...)):
    try:
        book = jsonable_encoder(book)
        new_book = await collection.insert_one(book)
        created_book = await collection.find_one({"_id": new_book.inserted_id})
        return created_book
    except DuplicateKeyError:
        # Handle duplicate key errors
        return {"error": "Duplicate key error."}
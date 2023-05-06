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

# Helper Function 
def book_helper(book) -> dict:
    return {
        "book_id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "description": book["description"],
        "price": book["price"],
        "stock": book["stock"],
    }

# Retrieves a list of all books in the store
@app.get("/books", response_description="List all books")
async def get_books():
    books = []
    async for book in collection.find(limit=100):
        books.append(book_helper(book))
    return books

# Retrieves a specific book by ID
@app.get("/books/{book_id}", response_description="List a specific book by ID")
async def get_book(book_id: str) -> dict:
    book = await collection.find_one({"_id": book_id})
    if book:
        return book_helper(book)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {book_id} not found.")
    

# Adds a new book to the store
@app.post("/books", response_description="Add a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
async def add_book(book: Book = Body(...)):
    try:
        book = jsonable_encoder(book)
        new_book = await collection.insert_one(book)
        created_book = await collection.find_one({"_id": new_book.inserted_id})
        return created_book
    except DuplicateKeyError:
        # Handle duplicate key errors
        return {"error": "Duplicate key error."}
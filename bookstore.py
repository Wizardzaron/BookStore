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

#Updates book   
@app.put("/books/{book_id}", response_description = "Update a pre-existing book")
async def update_book(book_id: str) -> dict:
    book = await collection.findOne({"_id": book_id})
    if book:
        db.collection.updateOne({ "_id": book_id }, {"$set": { "price": 19.95 } })
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Book with ID {book_id} not found")

#Deletes book

@app.delete("/books/{book_id}", response_description = "Delete a book")
async def delete_book(book_id: str) -> dict:
    book = await collection.findOne({"_id": book_id})
    if book:
        db.collection.deleteOne({"_id": book_id})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {book_id} not found.")

#finds book based on price, author, and title

# @app.get("/search?title={}&author={}&min_price={}&max_price={}", response_description = "Finding book based of price range, title, and author")
# async def search_books(book_id: str) -> dict:
#     books = []
#     async for book in collection.find("$or" [{"author": "Peter Attita"}, {}]):

#Finding all the books
@app.get("/all")
async def find_all_books():
    books = list(db.collection.aggregate([{"$match":{}}]))
    return books

#Top 5 authors based on the most amount of stock available
@app.get("/author")
async def best_authors():

#this group each individual tuple or doc into a single list based on their total stock with their id being their author 
# then organizes it in desending with the top 5 being the authors with the most amount of stock

#-1 means that we're sorting via descending order
    sorting = [{"$group":{"_id": "$author", "total_stock" : {"$sum": "$stock"}}}, {"$sort": {"total stock", -1}}, {"$limit": 5}]
    authors = list(db.collection.aggregate(sorting))
    return authors

#Top 5 best selling books based on how much stock is left (the lower the better selling)
@app.get("/best")
async def best_authors():

#this group each individual tuple or doc into a single list based on their lowest amount of stock with their id being
# their book title then organizes it in ascending with the top 5 being the title of the books that are the best sellers 
# which are the ones with the lowest amount of stock

#1 means that we're sorting via ascending order
    sorting = [{"$group":{"_id": "$title", "total_stock" : {"$sum": "$stock"}}}, {"$sort": {"total stock", 1}}, {"$limit": 5}]
    bestSellers = list(db.collection.aggregate(sorting))
    return bestSellers
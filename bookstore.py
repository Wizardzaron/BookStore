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

# Helper Function For some API endpoints
def book_helper(book) -> dict:
    return {
        "book_id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "description": book["description"],
        "price": book["price"],
        "stock": book["stock"],
    }

# MAIN API ENDPOINTS

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

# Updates an existing book by ID   
@app.put("/books/{book_id}", response_description = "Update a pre-existing book", response_model=BookUpdate)
async def update_book(book_id: str, book: BookUpdate = Body(...)):
    book = { key: value for key, value in book.dict().items() if value is not None }

    if len(book) >= 1:
        update_result = await collection.update_one({"_id": book_id}, {"$set": book})

        if update_result.modified_count == 1:
            if (updated_book := await collection.find_one({"_id": book_id})) is not None:
                return updated_book
        
    if (existing_book := await collection.find_one({"_id": book_id})) is not None:
        return existing_book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {book_id} not found.")

# Deletes a book from store by ID
@app.delete("/books/{book_id}", response_description = "Delete a book")
async def delete_book(book_id: str):
    book = await collection.find_one({"_id": book_id})
    if book:
        await collection.delete_one({"_id": book_id})
        return f"Book with ID: {book_id} removed. Book deleted successfully."
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {book_id} not found.")

# Searches for books by title, author, and price range
@app.get("/search_books")
async def search_books(title: str | None = None, 
                       author: str | None = None, 
                       min_price: float | None = None, 
                       max_price: float | None = None):
    
    print(f"Searching for book with title: {title}, author: {author}, min_price: {min_price}, max_price: {max_price}")

    # USER DID NOT INPUT ANYTHING, RETURN NOTHING
    if (title is None) and (author is None) and (min_price is None) and (max_price is None):
        return {"Search for books by title, author, and/or price range.", "No Seach Parameters Given."}

    # Combination Size ONE (SHOULD BE 4 Combinations)
    if (title is not None) and (author is None) and (min_price is None) and (max_price is None):
        print("USING COMBINATION SIZE ONE")
        return await collection.find({"title": title}).to_list(length=None)
    if (author is not None) and (title is None) and (min_price is None) and (max_price is None):
        print("USING COMBINATION SIZE ONE")
        return await collection.find({"author": author}).to_list(length=None)
    if (min_price is not None) and (title is None) and (author is None) and (max_price is None):
        print("USING COMBINATION SIZE ONE")
        return await collection.find({"price": { "$gt": min_price } }).to_list(length=None)
    if (max_price is not None) and (title is None) and (author is None) and (min_price is None):
        print("USING COMBINATION SIZE ONE")
        return await collection.find({"price": { "$lt": max_price } }).to_list(length=None)

    
    # Combination Size TWO (SHOULD BE 6 Combinations)
    if None not in (title, author):
        print("USING COMBINATION SIZE TWO")
        pipeline = [ {"$match": { "$and": [{ "title": title }, { "author": author }] } }]
    elif None not in (title, min_price):
        print("USING COMBINATION SIZE TWO")
        pipeline = [ {"$match": { "$and": [{ "title": title }, { "price": { "$gt": min_price } }] } }]
    elif None not in (title, max_price):
        print("USING COMBINATION SIZE TWO")
        pipeline = [ {"$match": { "$and": [{ "title": title }, { "price": { "$lt": max_price } }] } }]
    elif None not in (author, min_price):
        print("USING COMBINATION SIZE TWO")
        pipeline = [ {"$match": { "$and": [{ "author": author }, { "price": { "$gt": min_price} }] } }] 
    elif None not in (author, max_price):
        print("USING COMBINATION SIZE TWO")
        pipeline = [ {"$match": { "$and": [{ "author": author }, { "price": { "$lt": max_price } }] } }]
    elif None not in (min_price, max_price):
        print("USING COMBINATION SIZE TWO")
        pipeline = [ {"$match": { "$and": [{ "price": { "$gt": min_price, "$lt": max_price } }] } }]

    
    # Combination Size THREE (SHOULD BE 4 Combinations)
    if None not in (title, author, min_price):
        print("USING COMBINATION SIZE THREE")
        pipeline = [ {"$match": { "$and": [{ "title": title }, { "author": author }, { "price": { "$gt": min_price } }] } }]
    elif None not in (title, author, max_price):
        print("USING COMBINATION SIZE THREE")
        pipeline = [ {"$match": { "$and": [{ "title": title }, { "author": author }, { "price": { "$lt": max_price } }] } }]
    elif None not in (title, min_price, max_price):
        print("USING COMBINATION SIZE THREE")
        pipeline = [ {"$match": { "$and": [{ "title": title }, { "price": { "$gt": min_price, "$lt": max_price } }] } }]
    elif None not in (author, min_price, max_price):
        print("USING COMBINATION SIZE THREE")
        pipeline = [ {"$match": { "$and": [{ "author": author }, { "price": { "$gt": min_price, "$lt": max_price } }] } }]


    
    # Combination Size FOUR (SHOULD BE 1 Combination)
    if None not in (title, author, min_price, max_price):
        print("USING COMBINATION SIZE FOUR")
        pipeline = [ {"$match": { "$and": [{ "title": title }, { "author": author }, { "price": { "$gt": min_price, "$lt": max_price } }] } }]


    books = []
    async for doc in collection.aggregate(pipeline):
        books.append(doc)
    if books:
        return books
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"Method didn't work or No book found with current search queries")



# AGGREGATIONS

# The total number of (unique) books in store
@app.get("/total_number_books")
async def total_number_books():
    count = await collection.aggregate([{"$match": {}}, {"$group": {"_id": "null", "TotalNumberBooks": {"$sum": 1}}}]).to_list(length=None)
    return count

# The total number of books (based on stock) in store
@app.get("/total_number_stock")
async def total_number_stock():
    count = await collection.aggregate([{"$match": {}}, {"$group": {"_id": "null", "TotalNumberStock": {"$sum": "$stock"}}}]).to_list(length=None)
    return count

# Top 5 best selling books 
# based on how much stock is left (the lower the better selling)

# this group each individual tuple or doc into a single list based on their lowest amount of stock with their id being
# their book title then organizes it in ascending with the top 5 being the title of the books that are the best sellers 
# which are the ones with the lowest amount of stock

#1 means that we're sorting via ascending order
@app.get("/bestselling_books")
async def bestselling_books():
    pipeline = [{"$group": {"_id": {"title": "$title"},"total_stock": { "$sum": "$stock" }}},
                {"$sort": {"total_stock": 1 }},
                {"$limit": 5}]
    
    books = []
    async for doc in collection.aggregate(pipeline):
        books.append(doc)
    if books:
        return books
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"Method didn't work")

# Top 5 authors based on the most amount of stock available
# this group each individual tuple or doc into a single list based on their total stock with their id being their author 
# then organizes it in desending with the top 5 being the authors with the most amount of stock

#-1 means that we're sorting via descending order
@app.get("/authors_most_books")
async def authors_most_books():
    pipeline = [{"$group": {"_id": {"author": "$author"},"total_stock": { "$sum": "$stock" }}},
                {"$sort": {"total_stock": -1 }},
                {"$limit": 5}]
    
    authors = []
    async for doc in collection.aggregate(pipeline):
        authors.append(doc)
    if authors:
        return authors
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"Method didn't work")
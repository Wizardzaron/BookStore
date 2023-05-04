from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# currently, all fields are required
class Book(BaseModel):
    id: int # not sure if this one is needed
    title: str
    author: str
    description: str
    price: float
    stock: int

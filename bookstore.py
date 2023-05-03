from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List

app = FastAPI()
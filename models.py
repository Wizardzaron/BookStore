import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Book(BaseModel):
    book_id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    description: str = Field(...)
    price: float = Field(..., ge=0.0)
    stock: int = Field(..., ge=0)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "f488274f-d402-464d-8982-f60e2b612c2f",
                "title": "Outlive: The Science and Art of Longevity",
                "author": "Peter Attia",
                "description": "A look at recent scientific research on aging and longevity.",
                "price": 18.99,
                "stock": 0
            }
        }

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "title": "I'm Glad My Mom Died",
                "author": "Jennette McCurdy",
                "description": "The actress and filmmaker describes her eating disorders and difficult relationship with her mother.",
                "price": 125.99,
                "stock": 49115
            }
        }
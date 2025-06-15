# app/models/product_summary_model.py
from pydantic import BaseModel, Field

class ProductQuantity(BaseModel):
    product_name: str = Field(..., example="Laptop Pro X")
    quantity: int = Field(..., example=150)
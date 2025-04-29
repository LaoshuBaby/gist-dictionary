from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


class ProductBase(BaseModel):
    name: str
    description: str
    price: float


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ProductInDB(ProductBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Product(ProductInDB):
    pass


class ProductList(BaseModel):
    products: List[Product]
    total: int
    page: int
    limit: int
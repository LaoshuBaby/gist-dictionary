from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from db import db
from middleware.auth import get_api_key
from models.product import Product, ProductCreate, ProductList, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductList)
async def get_products(
    skip: int = 0, 
    limit: int = 100, 
    api_key: str = Depends(get_api_key)
):
    products = db.get_products(skip=skip, limit=limit)
    return {
        "products": products,
        "total": len(db.products),
        "page": skip // limit + 1 if limit > 0 else 1,
        "limit": limit
    }


@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: str, 
    api_key: str = Depends(get_api_key)
):
    product = db.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product


@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate, 
    api_key: str = Depends(get_api_key)
):
    return db.create_product(product)


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: str, 
    product: ProductUpdate, 
    api_key: str = Depends(get_api_key)
):
    updated_product = db.update_product(product_id, product)
    if updated_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str, 
    api_key: str = Depends(get_api_key)
):
    success = db.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return None
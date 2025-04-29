from datetime import datetime
import uuid
from typing import Dict, List, Optional, Union

from models.user import User, UserCreate, UserUpdate
from models.product import Product, ProductCreate, ProductUpdate


class InMemoryDB:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.products: Dict[str, Product] = {}

    # User operations
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return list(self.users.values())[skip:skip + limit]
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)
    
    def create_user(self, user: UserCreate) -> User:
        user_id = str(uuid.uuid4())
        now = datetime.now()
        db_user = User(
            id=user_id,
            username=user.username,
            email=user.email,
            created_at=now,
            updated_at=now
        )
        # In a real application, we would hash the password
        # For simplicity, we're not storing the password in the returned user object
        self.users[user_id] = db_user
        return db_user
    
    def update_user(self, user_id: str, user: UserUpdate) -> Optional[User]:
        db_user = self.users.get(user_id)
        if db_user is None:
            return None
        
        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        db_user.updated_at = datetime.now()
        self.users[user_id] = db_user
        return db_user
    
    def delete_user(self, user_id: str) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    # Product operations
    def get_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return list(self.products.values())[skip:skip + limit]
    
    def get_product(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id)
    
    def create_product(self, product: ProductCreate) -> Product:
        product_id = str(uuid.uuid4())
        now = datetime.now()
        db_product = Product(
            id=product_id,
            name=product.name,
            description=product.description,
            price=product.price,
            created_at=now,
            updated_at=now
        )
        self.products[product_id] = db_product
        return db_product
    
    def update_product(self, product_id: str, product: ProductUpdate) -> Optional[Product]:
        db_product = self.products.get(product_id)
        if db_product is None:
            return None
        
        update_data = product.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        
        db_product.updated_at = datetime.now()
        self.products[product_id] = db_product
        return db_product
    
    def delete_product(self, product_id: str) -> bool:
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False


# Create a singleton instance
db = InMemoryDB()
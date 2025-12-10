from typing import Optional
from pymongo import MongoClient
from bson import ObjectId

from app.aplication.ports.user_repository import UserRepository
from app.domain.entities.user import User
from app.infrastructure.config.settings import MONGO_URI

class MongoUserRepository(UserRepository):
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client["auth_db"]
        self.collection = self.db["users"]

    def get_by_email(self, email: str) -> Optional[User]:
        doc = self.collection.find_one({"email": email})
        return User.from_dict(doc) if doc else None
    
    def create(self, user: User):
        data = user.to_dict()
        result = self.collection.insert_one(data)
        user.id = str(result.insert_id)
        return user
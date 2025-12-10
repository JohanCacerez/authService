from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from bson import ObjectId

@dataclass
class User:
    id: Optional[str]
    email: str
    password_hash: str
    created_at: str

    @staticmethod
    def create_new(email: str, password_hash: str):
        now = datetime.now(datetime.timezone.utc).isoformat() + 'Z'
        return User(
            id=None,
            email=email,
            password_hash=password_hash,
            created_at=now
        )
    
    def to_dict(self):
        d = asdict(self)
        if self.id:
            d['id'] = ObjectId(self.id) if not ObjectId.is_valid(self.id) else ObjectId(self.id)
        d.pop('id', None)

        d["email"] = self.email
        d["password_hash"] = self.password_hash
        d["created_at"] = self.created_at
        return d
    
    @staticmethod
    def from_dict(d: dict):
        _id = d.get('_id') or d.get('id')
        id_str = str(_id) if _id is not None else None
        return User(
            id=id_str,
            email=d['email'],
            password_hash=d['password_hash'],
            created_at=d['created_at']
        )
from abc import ABC, abstractmethod
from typing import Optional, Tuple

class TokenService(ABC):
    @abstractmethod
    def generate_token(self, user_id:str) -> Tuple[str, int]:
        pass

    @abstractmethod
    def validate_token(self, token: str) -> Optional[str]:
        pass
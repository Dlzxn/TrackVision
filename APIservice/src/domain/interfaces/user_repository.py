from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.user import User

class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user in the data store."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their unique ID."""
        pass

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> List[User]:
        """Retrieve a list of users with pagination."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update an existing user's information."""
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        """Remove a user from the data store."""
        pass
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
C = TypeVar('C')
U = TypeVar('U')

class BaseRepository(ABC, Generic[T, C, U]):
    def __init__(self, db: AsyncSession, model_class: type):
        self.db = db
        self.model_class = model_class

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    async def create(self, entity_data: C) -> T:
        pass

    @abstractmethod
    async def update(self, entity_id: int, entity_data: U) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, entity_id: int) -> Optional[T]:
        pass
from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.domain.interfaces.user_repository import AbstractUserRepository
from src.infrastructure.repositories.user_repository import SQLAlchemyUserRepository

class AppProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, db_url: str):
        super().__init__()
        self.engine = create_async_engine(db_url)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    @provide(scope=Scope.APP)
    def get_engine(self):
        return self.engine

    @provide
    async def get_session(self) -> AsyncIterable[AsyncSession]:
        async with self.session_factory() as session:
            yield session

    user_repo = provide(SQLAlchemyUserRepository, provides=AbstractUserRepository)
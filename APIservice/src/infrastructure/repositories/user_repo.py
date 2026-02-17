from typing import Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.interfaces.user_repository import AbstractUserRepository
from src.domain.models.user import User as DomainUser
from src.infrastructure.db.user import UserORM

class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: DomainUser) -> DomainUser:
        db_user = UserORM(
            name=user.name,
            email=user.email,
            password=user.password,
            tg_id=user.tg_id,
            tg_username=user.tg_username
        )
        self.session.add(db_user)
        await self.session.flush()
        user.id = db_user.id
        return user

    async def get_by_id(self, user_id: int) -> Optional[DomainUser]:
        query = select(UserORM).where(UserORM.id == user_id)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[DomainUser]:
        query = select(UserORM).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self._to_domain(row) for row in result.scalars()]

    async def update(self, user: DomainUser) -> DomainUser:
        stmt = (
            update(UserORM)
            .where(UserORM.id == user.id)
            .values(
                name=user.name,
                email=user.email,
                password=user.password,
                tg_id=user.tg_id,
                tg_username=user.tg_username
            )
        )
        await self.session.execute(stmt)
        return user

    async def delete(self, user_id: int) -> None:
        stmt = delete(UserORM).where(UserORM.id == user_id)
        await self.session.execute(stmt)

    def _to_domain(self, orm_user: UserORM) -> DomainUser:
        return DomainUser(
            id=orm_user.id,
            name=orm_user.name,
            email=orm_user.email,
            password=orm_user.password,
            tg_id=orm_user.tg_id,
            tg_username=orm_user.tg_username
        )
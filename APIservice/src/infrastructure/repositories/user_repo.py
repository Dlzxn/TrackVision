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
        """Create user"""
        db_user = UserORM(
            name=user.name,
            email=user.email,
            password=user.password,
            tg_id=user.tg_id,
            tg_username=user.tg_username
        )
        self.session.add(db_user)
        await self.session.flush()
        await self.session.commit()
        user.id = db_user.id
        return user

    async def get_by_email(self, email: str) -> Optional[DomainUser]:
        query = select(UserORM).where(UserORM.email == email)
        result = await self.session.execute(query)
        user_orm = result.scalar_one_or_none()

        if user_orm:
            return self._to_domain(user_orm)
        
        return None

    async def get_by_name(self, username: str) -> Optional[DomainUser]:
        query = select(UserORM).where(UserORM.name == username)
        result = await self.session.execute(query)
        user_orm = result.scalar_one_or_none()

        if user_orm:
            return self._to_domain(user_orm)
        
        return None

    async def get_by_id(self, user_id: int) -> Optional[DomainUser]:
        """Get User by id"""
        query = select(UserORM).where(UserORM.id == user_id)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def get_all(self, limit: int = 10, offset: int = 0) -> List[DomainUser]:
        """Get all users with limit"""
        query = select(UserORM).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self._to_domain(row) for row in result.scalars()]

    async def update(self, user: DomainUser) -> DomainUser:
        """Update user """
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
        await self.session.commit()
        return user

    async def delete(self, user_id: int) -> None:
        """Delete User"""
        stmt = delete(UserORM).where(UserORM.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()

    def _to_domain(self, orm_user: UserORM) -> DomainUser:
        """Convert User"""
        return DomainUser(
            id=orm_user.id,
            name=orm_user.name,
            email=orm_user.email,
            password=orm_user.password,
            tg_id=orm_user.tg_id,
            tg_username=orm_user.tg_username
        )
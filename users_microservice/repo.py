from sqlalchemy import select
from db import UsersOrm, new_session
from schemas import SUserData, SUserAdd


class UserRepository:
    # Не планирую создавать экземрляр репозитория,
    # поэтому используя аннотацию classmethod
    @classmethod
    async def user_add(cls, data: SUserAdd) -> int:
        """
        Получение объекта типа SUserAdd и асинхронное
        добавление в БД. В ответ возвращает id
        созданного пользователя.
        """
        async with new_session() as session:
            user_data = data.model_dump()
            user = UsersOrm(**user_data)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def get_all(cls) -> list[SUserData]:
        """
        Получает всех пользователей бесплатного провадера
        и возвращает в виде коллекции элементов типа SUserData.
        """
        async with new_session() as session:
            q = select(UsersOrm)
            result = await session.execute(q)
            user_models = result.scalars().all()
            user_schemas = [
                SUserData.model_validate(user_model) for user_model in user_models
            ]
            return user_schemas

    @classmethod
    async def get_user(cls, user_id: int) -> SUserData:
        async with new_session() as session:
            q = select(UsersOrm).where(UsersOrm.id == user_id)
            result = await session.execute(q)
            user_model = result.scalars().one()
            user_schema = SUserData.model_validate(user_model)
            return user_schema

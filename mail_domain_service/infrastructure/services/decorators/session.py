from sqlalchemy.ext.asyncio import AsyncSession


def use_session(func):
    async def wrapper(self, *args, session: AsyncSession | None = None, **kwargs):
        if session is not None:
            return await func(self, *args, session=session, **kwargs)
        async with self._session_maker() as session:
            async with session.begin():
                return await func(self, *args, session=session, **kwargs)
    return wrapper

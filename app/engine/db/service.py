from datetime import datetime

from sqlalchemy import select, insert, func

from app.engine.db.models import Users

from app.engine.db.base import get_session


async def registrate_user(
        user_id: int,
        first_name: str | None,
        last_name: str | None,
):
    """registrate user if not exists else pass"""
    async with get_session() as session:
        res = await session.execute(
            select(Users).where(Users.user_id == user_id)
        )

        # user not exists
        if not res.scalar():
            await session.execute(
                insert(Users).values(
                    user_id=user_id,
                    first_name=first_name,
                    last_name=last_name
                )
            )

            await session.commit()

            return 1

        else:
            return 0


async def get_today_users() -> list[Users] | list:
    """get today registrated users"""
    async with get_session() as session:
        res = await session.execute(
            select(Users).filter(func.date(Users.reg_date) == datetime.date(datetime.today()))
        )

        res = res.all()

        return res if res else []

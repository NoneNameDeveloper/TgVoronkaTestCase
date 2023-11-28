from sqlalchemy import Column, BigInteger, String, DateTime

from sqlalchemy.orm import declarative_base

from datetime import datetime

Base = declarative_base()


class Users(Base):
    """таблица с пользователями, которые зарегистрированы в воронке"""
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, unique=True)  # ID Telegramm
    first_name = Column(String)  # имя
    last_name = Column(String)  # фамилия
    reg_date = Column(DateTime, default=datetime.now)  # время регистрации

from sqlalchemy import Column, Integer, String, DateTime

from sqlalchemy.orm import DeclarativeBase

from datetime import datetime

Base = DeclarativeBase()


class Users(Base):
    """таблица с пользователями, которые зарегистрированы в воронке"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, unique=True)  # ID Telegramm
    first_name = Column(String)  # имя
    last_name = Column(String)  # фамилия
    reg_date = Column(DateTime, default=datetime.now)  # время регистрации

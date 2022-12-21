from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, SmallInteger, VARCHAR, DATETIME, UniqueConstraint

UserBase = declarative_base()


class User(UserBase):
    __tablename__ = "test_users"
    __table_arg__ = (
        UniqueConstraint("email", name="email"),
        UniqueConstraint("username", name="ix_test_users_username"),
        {"mysql_charset": "utf8"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    surname = Column(VARCHAR(255), nullable=False)
    middle_name = Column(VARCHAR(255), nullable=True)
    username = Column(VARCHAR(16), nullable=True)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(64), nullable=False)
    access = Column(SmallInteger, nullable=True)
    active = Column(SmallInteger, nullable=True)
    start_active_time = Column(DATETIME, nullable=True)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, Integer, String, Text

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    created_on = Column(DateTime(timezone=True), default=db.func.now(), nullable=False)
    updated_on = Column(
        DateTime(timezone=True),
        default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False,
    )


class User(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(20), nullable=True)
    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)

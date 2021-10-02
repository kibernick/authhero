import uuid

from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, DateTime, Integer, String

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


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    first_name = Column(String(64), nullable=True)
    last_name = Column(String(64), nullable=True)
    password_hash = Column("password", String(128), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    api_keys = relationship(
        "ApiKey", back_populates="user", cascade="all, delete-orphan"
    )

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plaintext):
        self.password_hash = generate_password_hash(plaintext).decode("utf8")

    @classmethod
    def get_by_username(cls, username, is_active=True):
        return User.query.filter_by(
            username=username, is_active=is_active
        ).one_or_none()

    def is_correct_password(self, plaintext):
        return check_password_hash(self.password_hash, plaintext)

    def valid_api_keys(self):
        return ApiKey.query.filter_by(user=self, is_valid=True).all()


class ApiKey(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_valid = Column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="api_keys")

    @staticmethod
    def check_valid_key(key: str):
        try:
            uuid.UUID(key)
            return True
        except TypeError:
            return False

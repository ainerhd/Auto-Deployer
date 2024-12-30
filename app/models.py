from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default="NOW()")

    resources = relationship("UserResource", back_populates="user")


class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    node = Column(String, nullable=False)
    vmid = Column(Integer, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default="NOW()")

    users = relationship("UserResource", back_populates="resource")


class UserResource(Base):
    __tablename__ = "user_resources"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    role = Column(String, nullable=False)

    user = relationship("User", back_populates="resources")
    resource = relationship("Resource", back_populates="users")

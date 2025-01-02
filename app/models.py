from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Date, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    # Beziehungen
    resources = relationship("Resource", back_populates="owner")
    user_resources = relationship("UserResource", back_populates="user")
    user_info = relationship("UserInfo", back_populates="user", uselist=False)

class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    street = Column(String, nullable=True)
    street_number = Column(Integer, nullable=True)
    postal_code = Column(Integer, nullable=True)
    date_of_birth = Column(Date, nullable=True)

    # Beziehung
    user = relationship("User", back_populates="user_info")

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # VM oder LXC
    node = Column(String, nullable=False)
    vmid = Column(Integer, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Beziehungen
    owner = relationship("User", back_populates="resources")
    user_resources = relationship("UserResource", back_populates="resource")
    specs_lxc = relationship("SpecsLXC", back_populates="resource", uselist=False)
    specs_vm = relationship("SpecsVM", back_populates="resource", uselist=False)

class SpecsLXC(Base):
    __tablename__ = "specs_lxc"

    vmid = Column(Integer, ForeignKey("resources.vmid"), primary_key=True)
    password_hash = Column(String, nullable=True)
    node = Column(String, nullable=False)
    memory = Column(Integer, nullable=False)
    storage = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    net_name = Column(String, nullable=False)
    bridge = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    os = Column(String, nullable=False)
    cores = Column(Integer, nullable=False)
    nesting = Column(Integer, nullable=True)

    # Beziehung
    resource = relationship("Resource", back_populates="specs_lxc")

class SpecsVM(Base):
    __tablename__ = "specs_vm"

    vmid = Column(Integer, ForeignKey("resources.vmid"), primary_key=True)
    name = Column(String, nullable=False)
    cores = Column(Integer, nullable=False)
    memory = Column(Integer, nullable=False)
    scsi0 = Column(String, nullable=False)
    net0 = Column(String, nullable=False)
    node = Column(String, nullable=False)

    # Beziehung
    resource = relationship("Resource", back_populates="specs_vm")

class UserResource(Base):
    __tablename__ = "user_resources"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    role = Column(String, nullable=False)  # z. B. "Owner" oder "Viewer"

    # Beziehungen
    user = relationship("User", back_populates="user_resources")
    resource = relationship("Resource", back_populates="user_resources")

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String)
    role = Column(String)
    password = Column(String)
    phone = Column(String)
    address = Column(String)
    pets = relationship("Pet", back_populates="owner")  # No nullable parameter here

class Pet(Base):
    __tablename__ = "pets"
    id = Column(UUID(as_uuid=True), primary_key=True ,default=uuid.uuid4)
    name = Column(String)
    species = Column(String)
    breed = Column(String)
    colour = Column(String)
    isRegistered = Column(Boolean)
    gender = Column(String)
    nextVaccination = Column(Date)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # nullable here
    owner = relationship("User", back_populates="pets")
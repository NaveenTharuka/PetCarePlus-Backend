from sqlalchemy import Column, String, Boolean, ForeignKey, Date, DateTime, Time, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, time
import uuid
from sqlalchemy.sql import func


from app.database import Base
from sqlalchemy.types import Float


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=True)
    password = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    profile_pic_id = Column(UUID(as_uuid=True), ForeignKey("profile_pictures.id"), nullable=True)
    
    pets = relationship(
        "Pet",
        back_populates="owner",
        cascade="all, delete-orphan"
    )


class Pet(Base):
    __tablename__ = "pets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    image_url = Column(String, nullable=True)
    profile_pic_id = Column(UUID(as_uuid=True), ForeignKey("profile_pictures.id"), nullable=True)
    weight = Column(Float, nullable=True)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    colour = Column(String, nullable=True)
    is_registered = Column(Boolean, default=False)
    gender = Column(String, nullable=True)
    reports = relationship("Report", back_populates="pet", cascade="all, delete-orphan")
    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="pets")

    vaccinations = relationship(
        "Vaccination",
        back_populates="pet",
        cascade="all, delete-orphan"
    )

    vet_visits = relationship(
        "VetVisit",
        back_populates="pet",
        cascade="all, delete-orphan"
    )


class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    pet_id = Column(
        UUID(as_uuid=True),
        ForeignKey("pets.id"),
        nullable=False,
        index=True
    )

    vaccine_name = Column(String, nullable=False)
    vaccine_date = Column(Date, nullable=False)
    vet_name = Column(String, nullable=True)
    next_due_date = Column(Date, nullable=True)
    notes = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship("Pet", back_populates="vaccinations")

class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    pet = relationship("Pet", back_populates="reports")

class VetVisit(Base):
    __tablename__ = "vet_visits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    vet_name = Column(String, nullable=False)
    visit_date = Column(Date, nullable=False)
    reason = Column(String, nullable=False)
    note = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship("Pet", back_populates="vet_visits")  

class ProfilePictures(Base):
    __tablename__="profile_pictures"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    pet_id=Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=True)
    name = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Notification(Base):
    __tablename__="notifications"

    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    notification_type=Column(String, nullable=False)
    title=Column(String, nullable=False)
    messege=Column(String, nullable=False)
    icon=Column(String, nullable=False)
    read=Column(Boolean, default=False)
    created_at=Column(DateTime, default=datetime.utcnow)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    vet_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)

    reason = Column(String)

    status = Column(
        Enum(
            "Pending",
            "Confirmed",
            "Completed",
            "Cancelled",
            "Rejected",
            name="appointment_status"
        ),
        default="Pending"
    )

    notes = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
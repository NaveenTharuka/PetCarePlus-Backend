from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')

Base = declarative_base()

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("DB_URL not found in environment variables")

# DB_URL = "cockroachdb://naveen:SMoOIo5SEqVa5CeW_3Hn0w@racing-quagga-24604.j77.aws-ap-south-1.cockroachlabs.cloud:26257/defaultdb?sslmode=require"

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
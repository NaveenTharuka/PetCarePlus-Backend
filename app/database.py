from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
DB_URL = "postgresql://neondb_owner:npg_mHeniMWxL4p7@ep-bold-butterfly-a1149onp-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
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
from fastapi import FastAPI
from app.routes import userRoutes, petRoutes, fileRoutes
from app.database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(userRoutes.router)
app.include_router(petRoutes.router)
app.include_router(fileRoutes.router)

@app.get("/")
def welcome():
    return{"message": "Welcome to PetCare+"}
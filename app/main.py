from fastapi import FastAPI
from app.routes import userRoutes, petRoutes, fileRoutes, visitRoutes
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Include OPTIONS
    allow_headers=["*"],  # Allow all headers
)

app.include_router(userRoutes.router)
app.include_router(petRoutes.router)
app.include_router(fileRoutes.router)
app.include_router(visitRoutes.router)

@app.get("/")
def welcome():
    return{"message": "Welcome to PetCare+"}
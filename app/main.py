from fastapi import FastAPI
from app.routes import userRoutes, petRoutes, fileRoutes, visitRoutes, vaccineRoutes, notificationRoutes
from app.database import engine, Base
from app.websocket import websocketRoutes
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        os.getenv("FRONTEND_URL")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRoutes.router)
app.include_router(petRoutes.router)
app.include_router(fileRoutes.router)
app.include_router(visitRoutes.router)
app.include_router(vaccineRoutes.router)
app.include_router(notificationRoutes.router)
app.include_router(websocketRoutes.router)

@app.get("/")
def root():
    return {
        "success": True,
        "message": "PetCare Plus API is live 🐾",
        "server_time": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.head("/health")
def health():
    return {"status": "ok"}
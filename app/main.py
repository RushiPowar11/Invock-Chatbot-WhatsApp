from fastapi import FastAPI
from .database import Base, engine
from .routers import whatsapp

# Create tables on startup (prototype)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Invock WhatsApp Chatbot")

app.include_router(whatsapp.router, prefix="/webhook", tags=["whatsapp"])

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai_engine import generate_ai_response
from database import (
    initialize_database,
    save_message,
    get_chat_history
)
from memory_api import router as memory_router

import os
import uuid


# APP CONFIGURATION
app = FastAPI(
    title="KEYRADDIIN PERSONAL AI",
    description="Your Personal Intelligent Assistant",
    version="1.0.0"
)


# CORS CONFIGURATION
origins = os.getenv(
    "FRONTEND_ORIGIN",
    "http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type"]
)


# CONNECT MEMORY API
app.include_router(memory_router)


# DATABASE INITIALIZATION
@app.on_event("startup")
async def startup_event():
    initialize_database()
    print("KEYRADDIIN AI DATABASE INITIALIZED")


# CHAT REQUEST MODEL
class ChatRequest(BaseModel):
    message: str
    language: str = "auto"
    session_id: str | None = None


# HOME ROUTE
@app.get("/")
async def home():
    return {
        "project": "KEYRADDIIN PERSONAL AI",
        "status": "ONLINE",
        "version": "1.0.0"
    }


# HEALTH CHECK
@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "backend": "running",
        "database": "initialized",
        "ai_engine": "configured"
    }


# AI CHAT
@app.post("/api/chat")
async def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    session_id = request.session_id or str(uuid.uuid4())

    try:
        answer = generate_ai_response(
            message,
            request.language
        )

        save_message(
            session_id,
            "user",
            message
        )

        save_message(
            session_id,
            "assistant",
            answer
        )

        return {
            "success": True,
            "session_id": session_id,
            "response": answer,
            "ai_connected": True
        }

    except Exception as error:
        print("AI ERROR:", str(error))

        raise HTTPException(
            status_code=500,
            detail="AI service is temporarily unavailable."
        )


# CHAT HISTORY
@app.get("/api/history/{session_id}")
async def history(session_id: str):

    try:
        messages = get_chat_history(session_id)

        return {
            "success": True,
            "session_id": session_id,
            "history": messages
        }

    except Exception as error:
        print("HISTORY ERROR:", str(error))

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve chat history."
        )


# PROJECT INFORMATION
@app.get("/api/info")
async def information():

    return {
        "name": "KEYRADDIIN PERSONAL AI",
        "developer": "KEYRADDIIN MEDIA",
        "platform": "Web and Android PWA",
        "backend": "Python FastAPI",
        "ai": "Google Gemini",
        "memory": "Connected",
        "mode": "Online"
    }
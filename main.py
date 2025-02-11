from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import openai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load API Keys from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["chatbotDB"]
collection = db["chatHistory"]

# FastAPI App
app = FastAPI()

# CORS Middleware (Frontend ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model
class ChatRequest(BaseModel):
    user_id: str
    message: str

# Chatbot Logic using OpenAI API
@app.post("/chat/")
async def chat(request: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request.message}],
            api_key=OPENAI_API_KEY
        )

        bot_reply = response["choices"][0]["message"]["content"]

        # Save chat history in MongoDB
        chat_data = {
            "user_id": request.user_id,
            "user_message": request.message,
            "bot_reply": bot_reply
        }
        collection.insert_one(chat_data)

        return {"reply": bot_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root Route
@app.get("/")
def home():
    return {"message": "AI Chatbot Backend is Running!"}

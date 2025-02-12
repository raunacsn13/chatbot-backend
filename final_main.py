import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS Middleware Enable
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # या frontend का exact URL डालो
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        print("✅ Request Received:", request.dict())  # Debugging Log
        response_text = f"Bot reply to: {request.message}"
        print("✅ Response Sending:", response_text)  # Debugging Log
        return {"response": response_text}
    except Exception as e:
        print("❌ ERROR:", str(e))  # Error Log
        traceback.print_exc()  # पूरा Error Print करने के लिए
        raise HTTPException(status_code=500, detail=str(e))

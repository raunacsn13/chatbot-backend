import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS Middleware Enable
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # यहाँ पर frontend का exact URL डाल सकते हो
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
        print(f"✅ Received Request: {request}")  # Debugging Log
        response_text = f"Bot reply to: {request.message}"
        print(f"✅ Sending Response: {response_text}")  # Debugging Log
        return {"response": response_text}
    except Exception as e:
        print(f"❌ Error: {str(e)}")  # Error Logging
        traceback.print_exc()  # पूरा error log करने के लिए
        raise HTTPException(status_code=500, detail=str(e))

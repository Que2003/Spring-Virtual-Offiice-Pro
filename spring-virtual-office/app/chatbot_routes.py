import os
from fastapi import APIRouter
from pydantic import BaseModel

try:
    import anthropic
except ImportError:
    anthropic = None

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message

    if anthropic is None:
        return {
            "reply": "Anthropic is not installed. Add 'anthropic' to requirements.txt and redeploy."
        }

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        return {
            "reply": "ANTHROPIC_API_KEY is missing in Railway Variables."
        }

    client = anthropic.Anthropic(api_key=api_key)

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=800,
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        return {
            "reply": response.content[0].text
        }

    except Exception as e:
        return {
            "reply": f"AI error: {str(e)}"
        }

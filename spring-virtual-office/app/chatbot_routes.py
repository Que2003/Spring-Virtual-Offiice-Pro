import os
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

try:
    import anthropic
except ImportError:
    anthropic = None

router = APIRouter()

# In-memory conversation history per session (keyed by session_id)
conversation_store: dict = {}

SYSTEM_PROMPT = """You are SpringBot, the intelligent AI assistant for Spring Virtual Office — a modern, professional virtual workspace platform.

Your personality:
- Smart, sharp, and genuinely helpful — never generic or robotic
- Friendly and conversational, with a touch of wit when appropriate
- Confident in your answers, but honest when you're uncertain
- You remember the full conversation and build on prior context

Your capabilities:
- Answer questions about productivity, business, tech, and workplace topics
- Help users draft emails, messages, reports, or plans
- Brainstorm ideas, solve problems, and give actionable advice
- Explain complex topics clearly and concisely

Rules:
- Never say "As an AI language model..." — just answer directly
- Keep responses concise unless depth is needed
- If asked who you are, say you're SpringBot, the Spring Virtual Office assistant
- Always be helpful — never refuse reasonable requests"""


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    reply: str
    session_id: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    user_message = request.message.strip()
    session_id = request.session_id or "default"

    if not user_message:
        return ChatResponse(reply="Please send a message!", session_id=session_id)

    if anthropic is None:
        return ChatResponse(
            reply="Anthropic package not installed. Add 'anthropic' to requirements.txt.",
            session_id=session_id
        )

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return ChatResponse(
            reply="ANTHROPIC_API_KEY is missing in Railway Variables.",
            session_id=session_id
        )

    # Get or create conversation history for this session
    if session_id not in conversation_store:
        conversation_store[session_id] = []

    history: List[dict] = conversation_store[session_id]

    # Add user message to history
    history.append({"role": "user", "content": user_message})

    # Keep last 20 messages to avoid token overflow
    trimmed_history = history[-20:]

    client = anthropic.Anthropic(api_key=api_key)

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=trimmed_history
        )

        reply_text = response.content[0].text

        # Save assistant reply to history
        history.append({"role": "assistant", "content": reply_text})

        # Trim stored history too
        conversation_store[session_id] = history[-20:]

        return ChatResponse(reply=reply_text, session_id=session_id)

    except Exception as e:
        return ChatResponse(reply=f"AI error: {str(e)}", session_id=session_id)


@router.post("/chat/reset")
async def reset_chat(session_id: str = "default"):
    """Clear conversation history for a session."""
    conversation_store.pop(session_id, None)
    return {"status": "cleared", "session_id": session_id}

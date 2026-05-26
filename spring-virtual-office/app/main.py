from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.chatbot_routes import router as chatbot_router

app = FastAPI(title="Spring Virtual Office")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Spring Virtual Office</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                background: #0f172a;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                width: 90%;
                max-width: 720px;
                background: #111827;
                padding: 28px;
                border-radius: 18px;
                box-shadow: 0 0 40px rgba(0,0,0,0.5);
                display: flex;
                flex-direction: column;
                gap: 16px;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            h1 { color: #38bdf8; font-size: 22px; }
            .reset-btn {
                background: transparent;
                border: 1px solid #334155;
                color: #94a3b8;
                padding: 6px 14px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 13px;
                transition: all 0.2s;
            }
            .reset-btn:hover { border-color: #38bdf8; color: #38bdf8; }

            /* Chat history */
            .chat-history {
                background: #0f172a;
                border-radius: 12px;
                padding: 16px;
                min-height: 260px;
                max-height: 400px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            .msg {
                max-width: 85%;
                padding: 12px 16px;
                border-radius: 12px;
                font-size: 15px;
                line-height: 1.55;
                white-space: pre-wrap;
                word-break: break-word;
            }
            .msg.user {
                background: #1e3a5f;
                align-self: flex-end;
                border-bottom-right-radius: 3px;
            }
            .msg.bot {
                background: #1e293b;
                align-self: flex-start;
                border-bottom-left-radius: 3px;
                color: #e2e8f0;
            }
            .msg.thinking {
                color: #64748b;
                font-style: italic;
                background: transparent;
            }

            /* Input area */
            .input-row {
                display: flex;
                gap: 10px;
                align-items: flex-end;
            }
            textarea {
                flex: 1;
                height: 52px;
                max-height: 120px;
                border-radius: 10px;
                border: 1px solid #1e293b;
                background: #0f172a;
                color: white;
                padding: 14px;
                font-size: 15px;
                resize: none;
                outline: none;
                transition: border 0.2s;
                font-family: inherit;
            }
            textarea:focus { border-color: #38bdf8; }
            button.send-btn {
                padding: 14px 22px;
                background: #38bdf8;
                color: #020617;
                font-weight: bold;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-size: 15px;
                transition: background 0.2s;
                white-space: nowrap;
            }
            button.send-btn:hover { background: #0ea5e9; }
            button.send-btn:disabled { background: #1e3a5f; color: #475569; cursor: not-allowed; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌿 SpringBot</h1>
                <button class="reset-btn" onclick="resetChat()">Clear Chat</button>
            </div>

            <div class="chat-history" id="chatHistory">
                <div class="msg bot">Hey! I'm SpringBot, your Spring Virtual Office assistant. What can I help you with today?</div>
            </div>

            <div class="input-row">
                <textarea id="message" placeholder="Ask SpringBot anything..." onkeydown="handleKey(event)"></textarea>
                <button class="send-btn" id="sendBtn" onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            const SESSION_ID = 'session_' + Math.random().toString(36).substr(2, 9);

            function handleKey(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            }

            function appendMessage(text, role) {
                const history = document.getElementById('chatHistory');
                const msg = document.createElement('div');
                msg.className = 'msg ' + role;
                msg.innerText = text;
                history.appendChild(msg);
                history.scrollTop = history.scrollHeight;
                return msg;
            }

            async function sendMessage() {
                const input = document.getElementById('message');
                const sendBtn = document.getElementById('sendBtn');
                const message = input.value.trim();
                if (!message) return;

                appendMessage(message, 'user');
                input.value = '';
                sendBtn.disabled = true;

                const thinking = appendMessage('SpringBot is thinking...', 'bot thinking');

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message, session_id: SESSION_ID })
                    });
                    const data = await response.json();
                    thinking.className = 'msg bot';
                    thinking.innerText = data.reply;
                } catch (error) {
                    thinking.className = 'msg bot';
                    thinking.innerText = 'Connection error: ' + error.message;
                } finally {
                    sendBtn.disabled = false;
                    input.focus();
                }
            }

            async function resetChat() {
                await fetch('/chat/reset?session_id=' + SESSION_ID, { method: 'POST' });
                const history = document.getElementById('chatHistory');
                history.innerHTML = '<div class="msg bot">Chat cleared! What can I help you with?</div>';
            }
        </script>
    </body>
    </html>
    """

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
            body {
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }

            .container {
                width: 90%;
                max-width: 700px;
                background: #111827;
                padding: 30px;
                border-radius: 16px;
                box-shadow: 0 0 30px rgba(0,0,0,0.4);
            }

            h1 {
                text-align: center;
                color: #38bdf8;
            }

            textarea {
                width: 100%;
                height: 120px;
                border-radius: 10px;
                border: none;
                padding: 12px;
                font-size: 16px;
                resize: none;
            }

            button {
                width: 100%;
                margin-top: 15px;
                padding: 14px;
                background: #38bdf8;
                color: #020617;
                font-weight: bold;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background: #0ea5e9;
            }

            .reply {
                margin-top: 20px;
                background: #020617;
                padding: 18px;
                border-radius: 10px;
                min-height: 80px;
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Spring Virtual Office</h1>
            <textarea id="message" placeholder="Ask SpringBot something..."></textarea>
            <button onclick="sendMessage()">Send</button>
            <div class="reply" id="reply">SpringBot response will appear here.</div>
        </div>

        <script>
            async function sendMessage() {
                const message = document.getElementById("message").value;
                const replyBox = document.getElementById("reply");

                replyBox.innerText = "Thinking...";

                try {
                    const response = await fetch("/chat", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ message: message })
                    });

                    const data = await response.json();
                    replyBox.innerText = data.reply;
                } catch (error) {
                    replyBox.innerText = "Connection error: " + error.message;
                }
            }
        </script>
    </body>
    </html>
    """

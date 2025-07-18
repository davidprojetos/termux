from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat WebSocket</title>
</head>
<body>
    <h1>WebSocket Chat</h1>
    <input id="msg" type="text" placeholder="Digite uma mensagem" />
    <button onclick="sendMessage()">Enviar</button>
    <ul id="messages"></ul>
    <script>
        const ws = new WebSocket("ws://localhost:8000/ws");

        ws.onmessage = function(event) {
            const li = document.createElement("li");
            li.textContent = "Servidor: " + event.data;
            document.getElementById("messages").appendChild(li);
        };

        function sendMessage() {
            const input = document.getElementById("msg");
            ws.send(input.value);
            input.value = "";
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        msg = await websocket.receive_text()
        await websocket.send_text(f"Você disse: {msg}")

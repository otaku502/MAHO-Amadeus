from fastapi import FastAPI, WebSocket
from core.handler.ws_handler import WSHandler
from core.Amadeus import BaseAmadeus

app = FastAPI()

if __name__ == "__main__":
    ws_handler = WSHandler()
    Amadeus = BaseAmadeus()
    # 示例用法
    for token in Amadeus.llm.generate("你好"):
        print(token, end="", flush=True)

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await ws_handler.handle_ws(websocket, Amadeus)

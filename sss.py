import asyncio
import websockets

async def test_ws():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("已连接到服务器，输入内容并回车发送，直接回车退出。")
        while True:
            msg = input("输入: ")
            if not msg:
                print("已退出。")
                break
            await websocket.send(msg)
            try:
                response = await websocket.recv()
                print("收到:", response)
            except Exception as e:
                print(f"接收失败: {e}")
                break

asyncio.run(test_ws())
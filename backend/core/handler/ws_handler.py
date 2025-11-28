from starlette.websockets import WebSocketDisconnect
import logging
import asyncio
from core.util.message import process_message_queue

class WSHandler():
    def __init__(self):
        pass

    async def handle_ws(self, websocket, Amadeus):
        await websocket.accept()  # 必须先接受连接
        # 启动队列处理任务（调用工具类方法）
        processing_task = asyncio.create_task(process_message_queue(Amadeus, websocket))
        try:
            while True:
                data = await websocket.receive_text()
                for response in Amadeus.llm.generate(data):
                    await Amadeus.message_queue.put(response)
                logging.info(f"队列内容: {Amadeus.message_queue._queue} items")
                await websocket.send_text(f"成功收到: {data}")
        except WebSocketDisconnect:
            logging.info("WebSocket 已断开")
        finally:
            # 取消处理任务
            processing_task.cancel()
            try:
                await processing_task
            except asyncio.CancelledError:
                pass

    # process_queue 已移至 core.util.message 工具类

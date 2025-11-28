from starlette.websockets import WebSocketDisconnect
import logging
import asyncio
import re
import json


class WSHandler():
    def __init__(self):
        pass

    async def handle_ws(self, websocket, Amadeus):
        await websocket.accept()  # 必须先接受连接
        # 启动队列处理任务
        processing_task = asyncio.create_task(
            self.process_queue(Amadeus, websocket))
        try:
            while True:
                data = await websocket.receive_text()
                # 发送开始标签
                await websocket.send_text(json.dumps({"type": "start"}))
                for response in Amadeus.llm.generate(data):
                    await Amadeus.message_queue.put(response)
                logging.info(f"成功收到: {data}")
                # 等待队列处理完毕
                await Amadeus.message_queue.join()
                # 发送结束标签
                await websocket.send_text(json.dumps({"type": "end"}))
        except WebSocketDisconnect:
            logging.info("WebSocket 已断开")
        finally:
            # 取消处理任务
            processing_task.cancel()
            try:
                await processing_task
            except asyncio.CancelledError:
                pass

    async def process_queue(self, Amadeus, websocket):
        """
        循环处理消息队列：提取 -> 筛选 -> 组合 -> (TTS)
        """
        buffer = ""
        # 定义结束标点符号，用于断句
        sentence_endings = re.compile(r'[。！？.!?\n]+')

        while True:
            try:
                char = await Amadeus.message_queue.get()

                # 筛选掉没用的字符
                if not char or char in ["<think>", "</think>"]:
                    Amadeus.message_queue.task_done()
                    continue

                # 发送字符流（带标签）
                await websocket.send_text(json.dumps({"type": "text", "data": char}))
                buffer += char
                # 检查是否形成完整句子
                if sentence_endings.search(char):
                    sentence = buffer.strip()
                    if sentence:
                        logging.info(f"提取到句子: {sentence}")
                        # 调用 TTS 生成音频 (在线程池中运行以避免阻塞)
                        import base64
                        loop = asyncio.get_event_loop()
                        audio_data = await loop.run_in_executor(None, Amadeus.tts.generate_audio, sentence)
                        if audio_data:
                            audio_b64 = base64.b64encode(audio_data).decode()
                            await websocket.send_text(json.dumps({"type": "audio", "data": audio_b64}))
                            logging.info(f"已发送音频数据，长度: {len(audio_data)}")
                        else:
                            logging.warning("TTS 生成失败")
                    buffer = ""  # 清空缓冲区

                Amadeus.message_queue.task_done()

            except asyncio.CancelledError:
                raise
            except Exception as e:
                logging.error(f"队列处理出错: {e!r}")

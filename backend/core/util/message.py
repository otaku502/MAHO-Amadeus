import asyncio
import re
import logging

async def process_message_queue(Amadeus, websocket):
    """
    循环处理消息队列：提取 -> 筛选 -> 组合 -> (TTS)
    可直接在 handler 或其他地方调用。
    """
    buffer = ""
    sentence_endings = re.compile(r'[。！？.!?\n]+')
    while True:
        try:
            char = await Amadeus.message_queue.get()
            if not char:
                continue
            buffer += char
            if sentence_endings.search(char) or len(buffer) > 50:
                sentence = buffer.strip()
                if sentence:
                    logging.info(f"提取到句子: {sentence}")
                    loop = asyncio.get_event_loop()
                    audio_data = await loop.run_in_executor(None, Amadeus.tts.generate_audio, sentence)
                    if audio_data:
                        await websocket.send_bytes(audio_data)
                        logging.info(f"已发送音频数据，长度: {len(audio_data)}")
                    else:
                        logging.warning("TTS 生成失败")
                buffer = ""
            Amadeus.message_queue.task_done()
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logging.error(f"队列处理出错: {e}")

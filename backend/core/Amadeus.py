from pathlib import Path
import asyncio
from core.util.config import load_yaml
from core.component.llm.LLMService import LLM
from core.component.tts.TTSService import TTS


class BaseAmadeus:
    """
        Amadeus核心类，负责初始化和管理核心功能
    """

    def __init__(self):
        config_path = Path("config.yaml")
        self.config = load_yaml(config_path)
        self.llm = LLM(self.config.get("llm", {}))
        self.tts = TTS(self.config.get("tts", {}))

        self.message_queue = asyncio.Queue()  # 使用 asyncio.Queue 以支持异步操作

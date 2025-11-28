from pathlib import Path
from queue import Queue
from core.util.config import load_yaml
from core.component.llm.LLMService import LLM


class BaseAmadeus:
    """
        Amadeus核心类，负责初始化和管理核心功能
    """

    def __init__(self):
        config_path = Path("config.yaml")
        self.config = load_yaml(config_path)
        self.llm = LLM(self.config.get("llm", {}))

        self.message_queue = Queue()  # 用于存储消息的队列

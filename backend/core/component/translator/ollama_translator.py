import asyncio
from core.component.llm.ollama_api import Client as OllamaClient


class Client:
    """
    Ollama 翻译客户端，使用本地 LLM 模型进行翻译。
    支持小参数量模型，如 Qwen 0.5B，以追求性能。
    """

    def __init__(self, model: str = "qwen2.5:0.5b", base_url: str = "http://localhost:11434", **kwargs):
        """
        初始化 Ollama 翻译客户端。

        参数:
            model (str): Ollama 模型名称，默认使用 qwen2.5:0.5b (小参数量，性能优异)
            base_url (str): Ollama 服务地址，默认 localhost:11434
        """
        self.ollama_client = OllamaClient(model=model, base_url=base_url)
        self.model = model

    def translate(self, text: str, from_lang: str = "auto", to_lang: str = "ja") -> str:
        """
        翻译文本。

        参数:
            text (str): 要翻译的文本
            from_lang (str): 源语言 (目前模型自动检测)
            to_lang (str): 目标语言

        返回:
            str: 翻译后的文本
        """
        # 构建翻译提示词
        prompt = f"""请将以下文本翻译成{self._get_lang_name(to_lang)}：

{text}

直接输出翻译结果，不要添加任何解释或额外内容。"""

        # 异步调用 Ollama API
        async def _translate_async():
            response = ""
            async for token in self.ollama_client.generate(prompt, max_tokens=512, temperature=0.3):
                response += token
            return response.strip()

        # 运行异步任务
        try:
            return asyncio.run(_translate_async())
        except Exception as e:
            raise RuntimeError(f"Ollama 翻译失败: {e}")

    def _get_lang_name(self, lang_code: str) -> str:
        """
        将语言代码转换为中文名称。
        """
        lang_map = {
            "ja": "日语",
            "en": "英语",
            "zh": "中文",
            "ko": "韩语",
            "fr": "法语",
            "de": "德语",
            "es": "西班牙语",
            "it": "意大利语",
            "pt": "葡萄牙语",
            "ru": "俄语"
        }
        return lang_map.get(lang_code, lang_code)
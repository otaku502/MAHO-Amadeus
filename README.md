# MAHO-Amadeus

## 项目简介

MAHO-Amadeus 是一个灵感来源于《命运石之门》中阿玛丢斯系统的开源项目。目标是打造一个可扩展的虚拟角色交互框架，前端展示人物界面，用户可以与角色进行自然语言聊天。

本项目分为前端和后端两部分：
- **前端**：基于 Vue 3，负责角色形象展示、聊天界面交互。
- **后端**：基于 Python，负责对话逻辑、模型推理、数据处理等。

## 快速开始

1. 克隆仓库

2. 安装依赖（前端、后端）

3. 启动后端服务

4. 启动前端界面

---

# 本地tts和llm启动流程

## TTS（语音合成）服务启动流程

本项目支持对接 [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) 作为后端 TTS（文本转语音）服务，实现虚拟角色的声音克隆。

**启动流程简述：**

1. 前往 GPT-SoVITS 官方仓库下载并部署环境。
2. 准备好 SoVITS 和 GPT 语音模型权重，以及参考音频和文本。
3. 在 GPT-SoVITS 项目根目录下，使用如下命令启动 API 服务：
	```bash
	python api.py -dr "参考音频.wav" -dt "参考音频文本" -dl zh
	```
4. 启动后，TTS 服务会监听指定端口（默认 9880），可通过 HTTP 请求进行语音合成。
5. MAHO 后端可通过 HTTP 调用 TTS 服务，实现角色语音回复。

详细配置和模型训练请参考 [GPT-SoVITS 官方文档](https://github.com/RVC-Boss/GPT-SoVITS)。

---

## 便携环境快速启动（免安装依赖）

如果你下载的是 GPT-SoVITS 项目整合包，项目自带了一个 `runtime` 文件夹，里面包含了完整的 Python 便携环境。

你可以直接用这个环境启动 API 服务，无需安装 Anaconda 或 pip 依赖：

```powershell
cd D:\bysq_D\GPT-SoVITS-v2pro-20250604
./runtime/python.exe api.py -s SoVITS_weights_v2Pro/maho_e8_s528.pth -g GPT_weights_v2Pro/maho-e15.ckpt
```

这样可以直接启动，无需任何额外配置。

如果你用的是 WebUI，`go-webui.bat` 也是调用的这个 runtime 环境。

---

欢迎 Star、Fork、提交 Issue 或 PR，一起完善 MAHO-Amadeus

---

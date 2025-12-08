# MAHO-Amadeus

## 项目简介

MAHO-Amadeus 是一个灵感来源于《命运石之门》中阿玛丢斯系统的开源项目。目标是打造一个可扩展的虚拟角色交互框架，前端展示人物界面，用户可以与角色进行自然语言聊天。

本项目分为前端和后端和模型：
- **前端**：基于 Vue 3，负责角色形象展示、聊天界面交互。
- **后端**：基于 Python，负责对话逻辑、模型推理、数据处理等。
- **模型**: 一堆堆的模型服务，看个人喜好。

## 部署

### 前端部署 (Frontend)
1. **环境准备**：安装 Node.js (推荐 v18+)。
2. **安装依赖**：
   ```bash
   cd frontend
   npm install
   ```
3. **启动开发服务器**：
   ```bash
   npm run dev
   ```
这里我是习惯直接从发服务器启动，你喜欢的话也可以自己编译出来用，具体的话去看vue教程。

### 后端部署 (Backend)
1. **环境准备**：安装 Python 3.10+。
2. **安装依赖**：
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. **核心配置与扩展**：
   项目后端采用**组件化架构**，LLM、TTS、翻译等核心功能均可自由切换。修改 `backend/config.yaml` 即可灵活配置：
   核心代码位于backend\core\component\
   
   *   **模块化切换**：通过修改各板块的 `select` 字段（如 `ollama_api`, `gpt_sovits_api`）一键切换不同服务提供商。
   *   **LLM 配置**：默认支持 Ollama，可扩展接入 ChatGPT 等其他 API。
   *   **TTS 配置**：支持 GPT-SoVITS，可配置参考音频、语速等。
   *   **翻译配置**：支持多源切换（Ollama 本地大模型、百度 API、Argos 离线翻译）。
   
   > **特别提示**：若同时使用 Ollama 进行聊天(LLM)和翻译(Translator)，请务必设置环境变量 `OLLAMA_MAX_LOADED_MODELS=2` 并重启 Ollama，以防止模型反复加载导致显存冲突。
4. **启动服务**：
   ```bash
   python main.py
   ```

### LLM
[模型下载（基于qwen-14B微调）](https://www.modelscope.cn/models/bysq2006/maho-llm/files)
下载qwen3-14b.Q4_K_M.gguf 和 Modelfile
Modelfile 是用于配置和管理大语言模型（LLM）参数的文件，qwen3-14b.Q4_K_M.gguf是模型。下载后，你可以按照以下步骤使用：

1. 将 `Modelfile` 文件与 `qwen3-14b.Q4_K_M.gguf` 放在同一目录下。
2. 根据你的推理框架（如 Ollama、llama.cpp 等），在启动模型时指定 `Modelfile` 路径。例如，使用 Ollama 时可以运行：

  ```bash
  ollama create maho-llm -f ./Modelfile
  ```
3. 按照框架文档进一步配置和启动模型服务。

确保 `Modelfile` 中的参数与你的模型文件和硬件环境相匹配。具体配置说明可参考 [Ollama 官方文档](https://github.com/jmorganca/ollama/blob/main/docs/modelfile.md) 或相关推理框架的文档。


### TTS
[模型和环境下载](https://www.modelscope.cn/models/bysq2006/maho-tts/files)
在里面下载GPT-SoVITS-v2pro-20250604.zip
然后解压到喜欢的位置，

这里面自带了运行时环境./runtime/python.exe
解压好之后直接

cd 你的解压路径\GPT-SoVITS-v2pro-20250604
./runtime/python.exe api.py -s SoVITS_weights_v2Pro/maho_e8_s528.pth -g GPT_weights_v2Pro/maho-e15.ckpt

即可启动本地TTS

### 翻译（有LLM底层的，也有基于argos的，这里用LLM）



---

欢迎 Star、Fork、提交 Issue 或 PR，一起完善 MAHO-Amadeus

---

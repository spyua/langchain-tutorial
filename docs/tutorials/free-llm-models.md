# 免費 LLM 模型使用指南

::: warning 重要提醒
本指南中的所有模型都是開源且免費使用的，但請確保遵守各模型的授權條款，並在生產環境中評估其性能和安全性。
:::

## 概述

相較於需要付費的 OpenAI 模型，現在有許多高品質的開源 LLM 模型可以免費使用。這些模型可以分為兩大類：

1. **本地運行模型** - 在您的電腦上執行，完全免費且隱私安全
2. **託管免費模型** - 透過 Hugging Face 等平台提供的免費推理服務

## 本地運行模型：Ollama

### 什麼是 Ollama？

Ollama 是一個讓您能夠在本地運行大型語言模型的工具，支援 macOS、Windows 和 Linux。它提供了簡單的命令列介面，讓您能夠快速下載和運行各種開源模型。

### 2025年最新支援的模型

| 模型系列 | 參數大小 | 特色 | 適用場景 |
|---------|---------|------|---------|
| **Llama 3.3** | 70B | 新一代模型，接近 Llama 3.1 405B 的性能 | 高品質對話、多語言支援 |
| **Llama 3.2** | 11B, 90B | 支援視覺功能的模型 | 圖片理解、多模態應用 |
| **Llama 3.1** | 8B, 70B, 405B | 128K 上下文長度，多語言支援 | 長文本處理、程式碼生成 |
| **Llama 3** | 8B, 70B | 基礎版本，性能穩定 | 一般對話、文本生成 |
| **Mistral 7B** | 7B | 輕量化但高性能 | 快速推理、資源受限環境 |
| **CodeGemma** | 2B, 7B | 程式碼專用模型 | 程式碼生成、程式設計輔助 |

### 安裝 Ollama

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**macOS/Windows:**
前往 [ollama.com](https://ollama.com) 下載安裝程式

### 下載和運行模型

```bash
# 下載並運行 Llama 3.2 1B（推薦教學使用）
ollama run llama3.2:1b

# 下載並運行 Mistral 7B
ollama run mistral

# 列出已下載的模型
ollama list

# 移除不需要的模型
ollama rm llama3.2:1b
```

## Hugging Face 模型

### 熱門免費模型

| 模型名稱 | 開發者 | 參數大小 | 特色 | 授權 |
|---------|--------|---------|------|------|
| **FLAN-T5** | Google | 220M - 11B | 指令微調模型，多任務性能佳 | Apache 2.0 |
| **Mistral-7B** | Mistral AI | 7B | 超越 Llama 2 13B 的性能 | Apache 2.0 |
| **Zephyr-7B** | Hugging Face | 7B | Mistral-7B 的微調版本 | MIT |
| **CodeT5+** | Salesforce | 220M - 16B | 程式碼生成專用 | BSD-3 |
| **BLOOM** | BigScience | 560M - 176B | 多語言模型 | RAIL License |

### 模型選擇建議

**輕量級應用 (< 4GB RAM):**
- FLAN-T5 Small/Base
- DistilBERT 系列

**中等應用 (4-16GB RAM):**
- Mistral-7B
- Llama 3 8B
- FLAN-T5 Large

**高性能應用 (16GB+ RAM):**
- Llama 3.1 70B
- BLOOM 176B

## LangChain 整合

### 1. 使用 Ollama 模型

```python
# 安裝依賴
pip install langchain-ollama

# 基本使用
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2:1b")  # 推薦教學使用
response = llm.invoke("解釋什麼是機器學習")
print(response)
```

### 2. 使用 Hugging Face 模型

```python
# 安裝依賴
pip install langchain-huggingface transformers torch

# 使用 Hugging Face Pipeline
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_id = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

pipe = pipeline(
    "text-generation", 
    model=model, 
    tokenizer=tokenizer, 
    max_new_tokens=100
)

hf_llm = HuggingFacePipeline(pipeline=pipe)
response = hf_llm.invoke("你好，請介紹一下人工智慧")
print(response)
```

### 3. 使用 Hugging Face Endpoint

```python
# 透過 Hugging Face Inference API (免費額度)
from langchain_huggingface import HuggingFaceEndpoint
import os

# 設定 Hugging Face API Token (免費註冊取得)
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "your_token_here"

llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-large",
    model_kwargs={"temperature": 0.7, "max_length": 100}
)

response = llm.invoke("翻譯成中文：Hello, how are you?")
print(response)
```

### 4. 多模型鏈結使用

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 創建提示模板
prompt = PromptTemplate.from_template(
    "請用專業但易懂的方式解釋：{topic}"
)

# 創建處理鏈
chain = prompt | llm | StrOutputParser()

# 使用鏈結
result = chain.invoke({"topic": "量子計算"})
print(result)
```

## 環境設定最佳實踐

### 1. 虛擬環境設定

```bash
# 創建虛擬環境
python -m venv venv

# 啟動虛擬環境
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安裝基礎依賴
pip install langchain langchain-ollama langchain-huggingface
```

### 2. 依賴管理

建立 `requirements-free-models.txt`:

```txt
langchain>=0.1.0
langchain-ollama>=0.1.0
langchain-huggingface>=0.1.0
transformers>=4.35.0
torch>=2.0.0
tokenizers>=0.15.0
```

安裝：
```bash
pip install -r requirements-free-models.txt
```

### 3. 環境變數設定

建立 `.env` 檔案：

```bash
# Hugging Face Token (選用，用於提高 API 限制)
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here

# Ollama 設定 (通常使用預設值)
OLLAMA_HOST=http://localhost:11434
```

## 性能最佳化

### 硬體需求建議

| 模型大小 | 最低 RAM | 建議 RAM | CPU | GPU |
|---------|---------|---------|-----|-----|
| 7B 模型 | 8GB | 16GB | 4核心+ | 選用 |
| 13B 模型 | 16GB | 32GB | 8核心+ | 建議 |
| 70B 模型 | 64GB | 128GB | 16核心+ | 必要 |

### 量化模型

使用量化版本減少記憶體使用：

```bash
# 使用輕量級模型（推薦）
ollama run llama3.2:1b

# 或使用量化版本
ollama run llama3.1:8b-instruct-q4_0

# 查看可用的模型版本
ollama show llama3.2:1b
```

## 故障排除

### 常見問題

**1. 記憶體不足**
```python
# 使用輕量級模型（推薦）
llm = OllamaLLM(model="llama3.2:1b")

# 或使用中等模型
llm = OllamaLLM(model="llama3.1:8b")

# 或使用量化版本
llm = OllamaLLM(model="llama3.1:8b-instruct-q4_0")
```

**2. Ollama 連接錯誤**
```bash
# 檢查 Ollama 服務狀態
ollama list

# 重新啟動 Ollama 服務
sudo systemctl restart ollama  # Linux
# 或重新啟動應用程式 (macOS/Windows)
```

**3. Hugging Face 下載緩慢**
```python
# 使用鏡像站點
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
```

## 安全性考量

### 模型安全
- 評估模型輸出的品質和偏見
- 在生產環境中加入內容過濾
- 定期更新模型版本

### 隱私保護
- 本地模型不會將資料傳送到外部伺服器
- 使用 Hugging Face API 時注意資料隱私政策
- 敏感資料建議使用本地模型

## 總結

免費 LLM 模型為開發者提供了豐富的選擇：

- **Ollama**: 最佳的本地運行解決方案，隱私安全
- **Hugging Face**: 豐富的模型生態系統，易於實驗
- **LangChain 整合**: 統一的介面，便於切換模型

選擇模型時請考慮：硬體資源、應用需求、隱私要求和性能指標。

## 延伸閱讀

- [Ollama 官方文檔](https://ollama.com)
- [Hugging Face 模型庫](https://huggingface.co/models)
- [LangChain Ollama 整合](https://python.langchain.com/docs/integrations/llms/ollama)
- [開源 LLM 排行榜](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)
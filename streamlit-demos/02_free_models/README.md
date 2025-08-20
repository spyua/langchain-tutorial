# 免費 LLM 模型示範

這個 Streamlit 應用程式展示如何使用免費的開源 LLM 模型，包括本地運行的 Ollama 模型和 Hugging Face 託管的模型。

## 功能特色

- 🏠 **本地模型支援**: 整合 Ollama，在本地運行各種開源模型
- 🌐 **託管模型支援**: 使用 Hugging Face 的免費推理 API
- 🔄 **動態模型切換**: 輕鬆在不同模型間切換
- 📊 **性能監控**: 顯示回應時間和模型資訊
- 🛡️ **錯誤處理**: 完善的錯誤提示和安裝指南

## 支援的模型

### Ollama 本地模型
- Llama 3.1 (8B, 70B)
- Llama 3.2 (視覺模型)
- Mistral 7B
- CodeGemma
- 其他 Ollama 支援的模型

### Hugging Face 模型  
- FLAN-T5 (Small, Base, Large)
- DialoGPT (Small, Medium)
- DistilGPT2
- 其他開源模型

## 安裝需求

### Python 依賴
```bash
pip install streamlit langchain-ollama langchain-huggingface langchain-core requests
```

### Ollama 安裝 (選用)
```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# 下載模型
ollama pull llama3.1
```

## 使用方法

### 1. 啟動應用程式
```bash
cd streamlit-demos/02_free_models
streamlit run free_models_demo.py
```

### 2. 選擇模型類型
- **Ollama**: 需要先安裝 Ollama 並下載模型
- **Hugging Face**: 可選擇提供 API Token 以提高使用限制

### 3. 開始對話
- 選擇預設問題或輸入自訂問題
- 點擊「執行」按鈕獲得模型回應
- 查看處理時間和模型資訊

## 配置選項

### 環境變數
```bash
# Hugging Face API Token (選用)
export HUGGINGFACEHUB_API_TOKEN=your_token_here

# Ollama 服務地址 (預設)
export OLLAMA_HOST=http://localhost:11434
```

### 模型參數
- **Temperature**: 控制回應的創造性 (0.0-1.0)
- **Max Length**: 最大回應長度
- **Top-p**: 核心採樣參數

## 故障排除

### Ollama 相關問題

**問題**: 無法連接到 Ollama 服務
```bash
# 檢查服務狀態
ollama list

# 啟動服務
ollama serve
```

**問題**: 模型未找到
```bash
# 下載建議的模型
ollama pull llama3.1
ollama pull mistral
```

### Hugging Face 相關問題

**問題**: API 限制過低
- 註冊 Hugging Face 帳號
- 創建 API Token
- 在應用程式中輸入 Token

**問題**: 模型載入緩慢
- 選擇較小的模型 (如 FLAN-T5 Small)
- 檢查網路連接

## 硬體需求

### 本地模型 (Ollama)
| 模型大小 | 最低 RAM | 建議 RAM | 備註 |
|---------|---------|---------|------|
| 7B 模型 | 8GB | 16GB | 適合一般對話 |
| 13B 模型 | 16GB | 32GB | 更好的性能 |
| 70B 模型 | 64GB | 128GB | 需要高階硬體 |

### 託管模型 (Hugging Face)
- 無特殊硬體需求
- 需要穩定的網路連接
- 建議使用 API Token

## 安全性考量

### 本地模型
- ✅ 資料完全本地處理
- ✅ 無資料外洩風險
- ⚠️ 需要評估模型輸出品質

### 託管模型
- ⚠️ 資料會傳送到外部服務
- ⚠️ 需遵守服務提供商政策
- ✅ 由專業團隊維護

## 效能最佳化建議

### 本地模型
1. **使用量化模型**: 減少記憶體使用
   ```bash
   ollama pull llama3.1:8b-instruct-q4_0
   ```

2. **調整參數**: 平衡品質與速度
   ```python
   llm = OllamaLLM(
       model="llama3.1",
       temperature=0.3,  # 降低隨機性提高速度
   )
   ```

### 託管模型
1. **選擇合適大小**: 小模型回應更快
2. **批次處理**: 一次處理多個問題
3. **快取結果**: 避免重複請求

## 擴展功能

### 添加新模型
1. 在 `hf_models` 列表中添加模型名稱
2. 測試模型相容性
3. 更新文檔

### 自訂提示模板
```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "以專業但易懂的方式回答：{question}"
)

chain = prompt | llm
```

### 添加記憶功能
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
# 整合到對話鏈中
```

## 相關資源

- [Ollama 模型庫](https://ollama.com/library)
- [Hugging Face 模型中心](https://huggingface.co/models)
- [LangChain 文檔](https://python.langchain.com)
- [Streamlit 文檔](https://docs.streamlit.io)

## 授權聲明

本示範應用程式僅供教育用途。使用的模型可能有各自的授權條款，請在商業使用前確認相關授權。
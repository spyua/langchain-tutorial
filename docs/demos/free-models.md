# 免費模型展示

這個互動式 demo 展示如何使用各種免費的開源 LLM 模型，包括本地運行的 Ollama 模型和 Hugging Face 託管的模型。

## 🎯 展示功能

- **本地模型體驗**: 使用 Ollama 在本地運行 Llama、Mistral 等模型
- **託管模型測試**: 體驗 Hugging Face 的免費推理 API
- **性能比較**: 觀察不同模型的回應時間和品質
- **動態切換**: 輕鬆在不同模型間切換

## 🚀 快速開始

### 方法一：本地運行

```bash
# 進入 demo 目錄
cd streamlit-demos/02_free_models

# 安裝依賴
pip install -r requirements.txt

# 啟動應用程式
streamlit run free_models_demo.py
```

### 方法二：透過主選單

```bash
# 從專案根目錄啟動
streamlit run app.py

# 然後選擇「免費模型展示」
```

## 📋 前置需求

### Python 依賴
```txt
streamlit>=1.28.0
langchain-ollama>=0.1.0
langchain-huggingface>=0.1.0
langchain-core>=0.1.0
requests>=2.31.0
```

> **提示**: 若安裝失敗，請改用 `langchain-community` 並參考最新版 LangChain 文件。

### Ollama 設定 (選用)

如果想要體驗本地模型，需要安裝 Ollama：

```bash
# Linux/macOS 安裝
curl -fsSL https://ollama.com/install.sh | sh

# Windows 安裝
# 請前往 https://ollama.com 下載安裝程式
```

下載推薦的模型：

```bash
# 輕量級模型 (約 4GB)
ollama pull llama3.1:8b-instruct

# 中等模型 (約 8GB) 
ollama pull mistral:7b

# 程式碼專用模型
ollama pull codellama:7b

# 檢查可用的 tag
ollama list
```

### Hugging Face API Token (選用)

註冊 [Hugging Face](https://huggingface.co) 並創建 API Token 可以獲得更高的使用限制。

> **注意**: 免費 Token 雖能提高可用量，但仍有速率與流量上限（約每日 30 次 / 模型），需考慮升級方案或改用 Inference Endpoints。

## 🎮 使用指南

### 1. 選擇模型類型

**本地模型 (Ollama):**
- ✅ 完全免費，無使用限制
- ✅ 隱私安全，資料不外傳
- ✅ 離線使用
- ❌ 需要較多硬體資源
- ❌ 初次設定較複雜

**託管模型 (Hugging Face):**
- ✅ 無需本地資源
- ✅ 快速開始
- ✅ 多種模型選擇
- ❌ 需要網路連接
- ❌ 有使用限制

### 2. 模型推薦

| 用途 | 推薦模型 | 優點 |
|------|----------|------|
| 一般對話 | Llama 3.1 8B | 平衡的性能和速度 |
| 程式碼生成 | CodeLlama 7B | 專為程式設計優化 |
| 快速回應 | Mistral 7B | 輕量且高效 |
| 多語言支援 | FLAN-T5 Large | 支援多種語言任務 |

### 3. 測試問題建議

**對話測試:**
- 自我介紹
- 解釋複雜概念
- 創意寫作

**程式碼測試:**
- 寫簡單函數
- 程式碼除錯
- 演算法解釋

**知識問答:**
- 科學知識
- 歷史事件
- 技術解釋

## 🔧 進階設定

### 環境變數配置

創建 `.env` 檔案：

```bash
# Hugging Face API Token (選用)
HUGGINGFACEHUB_API_TOKEN=your_token_here

# Ollama 服務設定
OLLAMA_HOST=http://localhost:11434
# 注意: OLLAMA_TIMEOUT 需在程式碼或應用框架中支援，並非 Ollama 內建變數
OLLAMA_TIMEOUT=60
```

### 模型參數調整

您可以在 demo 中調整以下參數：

- **Temperature (0.0-1.0)**: 控制回應的創造性
- **Max Tokens**: 限制回應長度
- **Top-p**: 影響詞彙選擇的多樣性

## 🐛 常見問題

### Ollama 相關

**Q: 無法連接到 Ollama 服務**
```bash
# 檢查服務狀態
ollama list

# 手動啟動服務
ollama serve
```

**Q: 模型下載失敗**
```bash
# 檢查網路連接後重試
ollama pull llama3.1:8b-instruct

# 或嘗試其他來源
ollama pull llama3.1:8b-instruct-q4_0
```

**Q: 記憶體不足**
- 使用量化版本：`llama3.1:8b-instruct-q4_0`
- 關閉其他應用程式釋放記憶體
- 選擇較小的模型

### Hugging Face 相關

**Q: API 限制過低**
- 註冊並驗證 Hugging Face 帳號
- 創建和使用 API Token
- 選擇較小的模型減少請求量

**Q: 模型載入緩慢**
- 檢查網路連接
- 嘗試不同的模型
- 考慮使用本地模型

## 📊 性能參考

### 硬體需求 (本地模型)

| 模型大小 | 最低 RAM | 建議 RAM | 大約載入時間 |
|---------|---------|---------|-------------|
| 7B 模型 | 8GB | 16GB | 30-60 秒 |
| 13B 模型 | 16GB | 32GB | 1-2 分鐘 |
| 34B 模型 | 32GB | 64GB | 2-5 分鐘 |

> **硬體建議**: 建議搭配 GPU 使用，CPU-only 環境雖可運行，但推理速度會極慢。

### 回應時間參考

| 模型類型 | 平均回應時間 | 影響因素 |
|---------|-------------|----------|
| 本地 7B | 2-10 秒 | CPU/GPU 性能 |
| 本地 13B | 5-20 秒 | 記憶體頻寬 |
| HF Small | 1-3 秒 | 網路延遲 |
| HF Large | 3-10 秒 | 模型大小 |

## 🔗 相關資源

### 官方文檔
- [Ollama 官網](https://ollama.com)
- [Hugging Face Hub](https://huggingface.co/models)
- [LangChain 文檔](https://python.langchain.com)

### 模型庫
- [Ollama 模型庫](https://ollama.com/library)
- [Hugging Face 排行榜](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)

### 教學資源
- [免費 LLM 模型指南](/tutorials/free-llm-models)
- [環境設置教學](/demos/how-to-run)

---

> 💡 **提示**: 這個 demo 是了解不同免費模型特性的絕佳起點。建議先從較小的模型開始實驗，再根據需求選擇更大的模型。
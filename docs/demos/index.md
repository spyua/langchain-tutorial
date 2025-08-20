# Demo 展示

這裡提供可執行的 Streamlit 互動 Demo，讓您親手體驗 LangChain 的強大功能。

## 🎮 可用 Demo

### 01. Gemini 基礎聊天

一個使用 LangChain 整合 Google Gemini API 的基礎聊天應用程式。

**功能特色：**
- ✅ API 連接測試
- 🔧 多模型支援（gemini-1.5-flash、gemini-1.5-pro、gemini-1.0-pro）
- 💬 互動式聊天介面
- ⚙️ 動態配置參數
- 📊 回答統計資訊

**學習重點：**
- LangChain 與 Google Gemini 整合
- 環境變數管理
- 錯誤處理機制
- Streamlit UI 設計

[📖 詳細說明 →](/demos/gemini-chat)

## 🚀 如何執行 Demo

### 前置需求

1. **建立 Python 虛擬環境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # 或 venv\Scripts\activate  # Windows
   ```

2. **安裝 Python 依賴**
   ```bash
   pip install -r requirements.txt
   ```

3. **設置環境變數**
   ```bash
   # 創建 .env 檔案
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

4. **取得 Google API Key**
   - 前往 [Google AI Studio](https://aistudio.google.com/)
   - 建立新專案並取得 API Key

[📖 完整設置指南 →](/demos/how-to-run)

### 執行步驟

```bash
# 進入 Demo 目錄
cd streamlit-demos/01_gemini_basic

# 執行 Streamlit 應用
streamlit run gemini_chat.py
```

應用將在瀏覽器中開啟，通常是 `http://localhost:8501`

## 📖 Demo 架構說明

```
streamlit-demos/
└── 01_gemini_basic/
    ├── gemini_chat.py    # 主要應用程式
    └── README.md         # 詳細說明文件
```

每個 Demo 都是獨立的 Streamlit 應用，包含：
- **主程式檔案** - 完整的應用邏輯
- **說明文件** - 安裝與使用指南
- **範例代碼** - 可直接執行的程式

## 🔧 故障排除

### 常見問題

**問題：** `ModuleNotFoundError: No module named 'langchain_google_genai'`
**解決：** 
```bash
pip install langchain-google-genai
```

**問題：** API Key 驗證失敗
**解決：**
1. 檢查 API Key 是否正確
2. 確認 `.env` 檔案位於正確位置
3. 重新啟動 Streamlit 應用

**問題：** 連接逾時
**解決：**
1. 檢查網路連線
2. 確認 Google AI 服務狀態
3. 嘗試使用不同的模型

## 💡 擴展建議

基於這些 Demo，您可以：

1. **自定義聊天機器人** - 修改系統提示詞和參數
2. **整合其他模型** - 添加 OpenAI、Anthropic 等模型
3. **增加功能** - 加入記憶系統、工具整合等
4. **改善 UI** - 自定義 Streamlit 介面設計

---

::: tip 提示
建議先從 Gemini 基礎聊天 Demo 開始，熟悉基本操作後再探索更複雜的功能。
:::
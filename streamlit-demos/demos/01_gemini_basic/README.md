# Gemini 基礎聊天 Demo

這是一個使用 LangChain 整合 Google Gemini API 的基礎聊天應用程式。

## 功能特色

- ✅ Gemini API 連接測試
- 🤖 多模型支援 (gemini-1.5-flash, gemini-1.5-pro, gemini-1.0-pro)
- 💬 互動式聊天介面
- 🔧 API Key 動態配置
- 📊 回應統計資訊

## 執行方式

```bash
cd demos/01_gemini_basic
streamlit run gemini_chat.py
```

## 環境需求

確保已安裝所需套件：
```bash
pip install streamlit langchain langchain-google-genai python-dotenv
```

## 設定 API Key

1. 在專案根目錄創建 `.env` 文件
2. 添加您的 Google API Key：
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## 學習重點

- LangChain 與 Google Gemini 的整合
- Streamlit 建構聊天介面
- 動態模型選擇
- 錯誤處理最佳實踐
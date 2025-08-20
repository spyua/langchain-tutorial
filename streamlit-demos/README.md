# Streamlit Demo 說明

這個資料夾包含所有可執行的 Streamlit 互動 Demo。

## 📁 Demo 結構

```
streamlit-demos/
├── 01_gemini_basic/         # Gemini API 基礎聊天
│   ├── gemini_chat.py      # 主程式
│   └── README.md           # Demo 說明
└── README.md               # 這個檔案
```

## 🚀 執行方式

### 全域需求
```bash
# 安裝依賴 (在專案根目錄執行)
pip install -r requirements.txt

# 設置環境變數
cp .env.example .env
# 編輯 .env 加入你的 API Keys
```

### 執行個別 Demo
```bash
# 進入想要執行的 Demo 目錄
cd streamlit-demos/01_gemini_basic

# 執行 Streamlit 應用
streamlit run gemini_chat.py
```

## 📖 Demo 列表

### 01. Gemini 基礎聊天
- **檔案**: `01_gemini_basic/gemini_chat.py`
- **功能**: LangChain + Google Gemini API 整合
- **需求**: `GOOGLE_API_KEY`
- **學習重點**: 基礎模型調用、錯誤處理、UI 設計

## 🔧 開發建議

### 新增 Demo 的步驟
1. 在 `streamlit-demos/` 下建立新資料夾 (使用編號格式: `02_demo_name/`)
2. 創建主程式檔案 (建議命名與功能相關)
3. 加入 README.md 說明文件
4. 更新此檔案的 Demo 列表
5. 在 VitePress 文檔中加入相關說明

### Demo 設計原則
- **獨立性**: 每個 Demo 應該可以獨立執行
- **教育性**: 專注於特定 LangChain 功能的教學
- **互動性**: 提供豐富的用戶互動體驗
- **錯誤處理**: 包含完善的異常處理機制
- **說明文件**: 詳細的使用說明和學習重點

## 🐛 故障排除

### 常見問題

**問題**: 模組導入錯誤
```bash
ModuleNotFoundError: No module named 'langchain_google_genai'
```
**解決**: 確保已安裝所有依賴
```bash
pip install -r requirements.txt
```

**問題**: API Key 錯誤
```bash
AuthenticationError: Invalid API Key
```
**解決**: 檢查 `.env` 檔案中的 API Key 設置

**問題**: Streamlit 無法啟動
```bash
streamlit: command not found
```
**解決**: 確認 Streamlit 已正確安裝
```bash
pip install streamlit
```

## 📝 貢獻指南

歡迎貢獻新的 Demo 或改進現有的範例！

### 貢獻步驟
1. Fork 這個 Repository
2. 建立新的功能分支
3. 開發並測試你的 Demo
4. 更新相關文檔
5. 提交 Pull Request

### Demo 品質檢查
- [ ] 程式碼可以正常執行
- [ ] 包含適當的錯誤處理
- [ ] 有清楚的使用說明
- [ ] UI 設計友好
- [ ] 符合專案的程式碼風格

---

💡 **提示**: 建議先從現有的 Demo 開始學習，理解程式碼結構後再開發新功能。
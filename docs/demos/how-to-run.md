# 如何執行 Demo

本頁提供完整的環境設置和 Demo 執行指南。

## 📋 環境需求

- **Python 3.8+**
- **Node.js 16+** (用於 VitePress)
- **Git**

## 🔧 完整設置步驟

### 1. 複製專案
```bash
git clone https://github.com/your-username/langchain-tutorial.git
cd langchain-tutorial
```

### 2. 建立 Python 虛擬環境
```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. 安裝依賴套件
```bash
# 安裝 Python 依賴 (Streamlit Demos)
pip install -r requirements.txt

# 安裝 Node.js 依賴 (VitePress)
npm install
```

### 4. 設置環境變數
```bash
# 複製環境變數範本
cp .env.example .env

# 編輯 .env 檔案，加入你的 API Keys
# GOOGLE_API_KEY=your_google_api_key_here
```

## 🚀 執行應用

### VitePress 文檔網站
```bash
# 開發模式
npm run docs:dev
# 網站會在 http://localhost:5173 啟動
```

### Streamlit Demo
```bash
# 確保虛擬環境已啟動
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 執行本地 Demo 導航
streamlit run app.py
# 應用會在 http://localhost:8501 啟動

# 或執行個別 Demo
cd streamlit-demos/01_gemini_basic
streamlit run gemini_chat.py
```

## 🔑 API Key 設置

### Google Gemini API
1. 前往 [Google AI Studio](https://aistudio.google.com/)
2. 建立新專案或選擇現有專案
3. 生成 API Key
4. 將 Key 加入 `.env` 檔案：
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## 🐛 常見問題

### Python 虛擬環境問題
**問題**: `python -m venv venv` 失敗
**解決**: 
```bash
# Ubuntu/Debian
sudo apt install python3-venv

# macOS (使用 Homebrew)
brew install python3

# Windows
# 確保已安裝 Python 並加入 PATH
```

### 套件安裝問題
**問題**: `pip install` 失敗
**解決**:
```bash
# 更新 pip
pip install --upgrade pip

# 清除快取重新安裝
pip cache purge
pip install -r requirements.txt
```

### Node.js 問題
**問題**: `npm install` 失敗
**解決**:
```bash
# 清除 npm 快取
npm cache clean --force

# 刪除 node_modules 重新安裝
rm -rf node_modules package-lock.json
npm install
```

### API Key 問題
**問題**: API 驗證失敗
**解決**:
1. 檢查 `.env` 檔案是否在專案根目錄
2. 確認 API Key 格式正確（無多餘空格）
3. 驗證 API Key 在對應平台是否有效
4. 重新啟動 Streamlit 應用

### 埠口衝突
**問題**: 埠口已被使用
**解決**:
```bash
# VitePress 指定埠口
npm run docs:dev -- --port 3000

# Streamlit 指定埠口
streamlit run app.py --server.port 8502
```

## 📁 專案結構說明

```
langchain-tutorial/
├── venv/                     # Python 虛擬環境
├── docs/                     # VitePress 文檔
├── streamlit-demos/          # Streamlit 互動 Demo
├── node_modules/             # Node.js 依賴
├── requirements.txt          # Python 依賴清單
├── package.json             # Node.js 依賴清單
├── .env                     # 環境變數 (需自行建立)
└── .env.example             # 環境變數範本
```

## 💡 開發建議

### 虛擬環境管理
```bash
# 停用虛擬環境
deactivate

# 重新啟動虛擬環境
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 依賴管理
```bash
# 更新 requirements.txt
pip freeze > requirements.txt

# 檢查過期套件
pip list --outdated
```

### Git 忽略檔案
確保以下項目已加入 `.gitignore`：
```
venv/
node_modules/
.env
__pycache__/
*.pyc
.DS_Store
```

---

::: tip 小貼士
建議將這些指令寫成腳本檔案，方便團隊成員快速設置環境。
:::
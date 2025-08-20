# 建議的開發指令

## VitePress 文檔網站
```bash
# 開發伺服器
npm run docs:dev

# 建構生產版本
npm run docs:build

# 預覽生產版本
npm run docs:preview
```

## Streamlit 示例
```bash
# 本地示例導航
streamlit run app.py

# 個別示例 (以 Gemini 聊天為例)
cd streamlit-demos/01_gemini_basic
streamlit run gemini_chat.py
```

## 依賴安裝
```bash
# 1. 建立 Python 虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/macOS

# 2. 安裝 Python 依賴 (Streamlit 示例)
pip install -r requirements.txt

# 3. 安裝 Node.js 依賴 (VitePress)
npm install
```

## 環境設定
```bash
# 複製環境範本
cp .env.example .env

# 編輯 .env 檔案並添加 API 金鑰
# GOOGLE_API_KEY=your_actual_api_key_here
```

## Git 指令
```bash
git add .
git commit -m "描述訊息"
git push origin main
```
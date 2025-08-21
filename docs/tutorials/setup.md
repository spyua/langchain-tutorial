# 環境設置

本章節將指導您完成 LangChain 開發環境的設置，包括 Python 環境配置、套件安裝，以及免費和付費模型的配置選項。

## 🎯 設置目標

完成本章節後，您將擁有：
- ✅ 乾淨的 Python 開發環境
- ✅ 完整的 LangChain 套件安裝
- ✅ 免費模型配置（Ollama + Hugging Face）
- ✅ 付費模型配置（OpenAI、Google、Anthropic）
- ✅ 靈活的模型切換能力

## 📋 系統需求

### 基本需求
- **作業系統**: Windows 10+, macOS 10.14+, 或 Linux
- **Python**: 3.8 或更高版本
- **記憶體**: 最少 8GB RAM（推薦 16GB+）
- **儲存空間**: 至少 5GB 可用空間

### 推薦硬體配置
| 用途 | CPU | RAM | 儲存 | GPU |
|------|-----|-----|------|-----|
| 學習開發 | 4核心+ | 8GB+ | 256GB SSD | 選用 |
| 本地模型 | 8核心+ | 16GB+ | 512GB SSD | 建議 |
| 生產部署 | 16核心+ | 32GB+ | 1TB SSD | 必要 |

## 🐍 Python 環境設置

### 1. 檢查 Python 版本

```bash
# 檢查 Python 版本
python --version
# 或
python3 --version

# 應該顯示 3.8.x 或更高版本
```

### 2. 安裝 Python（如果需要）

**Windows:**
- 前往 [python.org](https://www.python.org/downloads/)
- 下載最新版本並安裝
- ✅ **重要**: 勾選 "Add Python to PATH"

**macOS:**
```bash
# 使用 Homebrew 安裝
brew install python

# 或使用官方安裝程式
# 前往 https://www.python.org/downloads/
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 3. 升級 pip

```bash
# 升級到最新版本
python -m pip install --upgrade pip
```

## 🌐 虛擬環境設置

::: tip 為什麼使用虛擬環境？
虛擬環境可以：
- 隔離不同專案的依賴
- 避免套件版本衝突
- 保持系統 Python 環境乾淨
- 便於專案部署和分享
:::

### 1. 創建虛擬環境

```bash
# 創建名為 langchain-env 的虛擬環境
python -m venv langchain-env

# 或指定 Python 版本
python3 -m venv langchain-env
```

### 2. 啟動虛擬環境

**Windows:**
```bash
# Command Prompt
langchain-env\Scripts\activate

# PowerShell
langchain-env\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source langchain-env/bin/activate
```

### 3. 確認虛擬環境已啟動

啟動後，命令提示符應該顯示：
```bash
(langchain-env) $ 
```

### 4. 停用虛擬環境

```bash
deactivate
```

## 📦 LangChain 套件安裝

### 1. 基礎套件安裝

```bash
# 確保虛擬環境已啟動
(langchain-env) $ pip install langchain langchain-core
```

### 2. 模型整合套件

#### 💰 付費模型套件

**OpenAI 模型:**
```bash
pip install langchain-openai
```

**Google Gemini 模型:**
```bash
pip install langchain-google-genai
```

**Anthropic Claude 模型:**
```bash
pip install langchain-anthropic
```

#### 🆓 免費模型套件

**本地 Ollama 模型:**
```bash
pip install langchain-ollama
```

**Hugging Face 免費模型:**
```bash
pip install langchain-huggingface transformers torch
```

#### 📦 完整安裝選項

**只安裝免費模型:**
```bash
pip install langchain-ollama langchain-huggingface transformers torch
```

**安裝所有模型支援:**
```bash
pip install langchain-openai langchain-google-genai langchain-anthropic langchain-ollama langchain-huggingface transformers torch
```

### 3. 額外功能套件

```bash
# 文檔處理
pip install pypdf python-docx

# 向量資料庫
pip install chromadb faiss-cpu

# 網頁開發
pip install streamlit gradio

# 環境變數管理
pip install python-dotenv

# 通用工具
pip install requests beautifulsoup4
```

### 4. 一次性完整安裝

建立 `requirements.txt` 文件：

```txt
# 核心套件
langchain>=0.1.0
langchain-core>=0.1.0

# 付費模型整合（選用）
langchain-openai>=0.1.0
langchain-google-genai>=0.1.0
langchain-anthropic>=0.1.0

# 免費模型整合
langchain-ollama>=0.1.0
langchain-huggingface>=0.1.0

# 機器學習
transformers>=4.35.0
torch>=2.0.0
numpy>=1.24.0

# 文檔處理
pypdf>=3.0.0
python-docx>=0.8.11

# 向量資料庫
chromadb>=0.4.0
faiss-cpu>=1.7.4

# 網頁框架
streamlit>=1.28.0

# 工具套件
python-dotenv>=1.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
```

安裝所有依賴：
```bash
pip install -r requirements.txt
```

## 🔑 API 金鑰與Token設定

### 1. 環境變數檔案設置

在專案根目錄創建 `.env` 檔案：

```bash
# 💰 付費模型 API 金鑰（選用）
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 🆓 免費模型 Token（選用，提高限制）
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here

# 🔍 開發工具（選用）
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key_here
```

### 2. 在程式中載入環境變數

```python
from dotenv import load_dotenv
import os

# 載入 .env 檔案
load_dotenv()

# 付費模型金鑰
openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# 免費模型 Token
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
```

### 3. 取得 API 金鑰

#### 💰 付費模型金鑰

**OpenAI API:**
1. 前往 [OpenAI Platform](https://platform.openai.com/)
2. 註冊帳號並綁定付費方式
3. 前往 API Keys 頁面
4. 點擊 "Create new secret key"
5. 複製金鑰並貼到 `.env` 檔案

**Google Gemini API:**
1. 前往 [Google AI Studio](https://aistudio.google.com/)
2. 登入 Google 帳號
3. 點擊 "Get API key"
4. 創建新的 API 金鑰
5. 複製金鑰並貼到 `.env` 檔案

**Anthropic Claude API:**
1. 前往 [Anthropic Console](https://console.anthropic.com/)
2. 註冊帳號並設置付費
3. 前往 API Keys 頁面
4. 創建新的金鑰
5. 複製金鑰並貼到 `.env` 檔案

#### 🆓 免費模型 Token

**Hugging Face Token:**
1. 前往 [Hugging Face](https://huggingface.co/)
2. 註冊並登入（完全免費）
3. 前往 Settings → Access Tokens
4. 創建新的 Read token
5. 複製並貼到 `.env` 檔案

::: tip 使用建議
- **初學者**: 先使用免費的 Ollama 和 Hugging Face 模型
- **進階用戶**: 根據需求選擇付費模型以獲得更好的性能
- **生產環境**: 建議使用付費模型以確保服務穩定性
:::

::: warning 安全提醒
- 永遠不要將 API 金鑰提交到 Git 儲存庫
- 將 `.env` 加入 `.gitignore` 檔案
- 定期更換 API 金鑰
- 為不同專案使用不同的金鑰
:::

## 🦙 本地模型設置 (Ollama)

### 1. 安裝 Ollama

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
前往 [ollama.com](https://ollama.com) 下載安裝程式

### 2. 啟動 Ollama 服務

```bash
ollama serve
```

### 3. 下載推薦模型

```bash
# 輕量級模型 (約 1.3GB) - 推薦教學使用
ollama pull llama3.2:1b

# 中等模型 (約 4GB)
ollama pull llama3.1:8b

# 程式碼專用模型
ollama pull codellama:7b

# 中等性能模型
ollama pull mistral:7b
```

### 4. 測試模型

```bash
# 測試對話 - 使用輕量級模型
ollama run llama3.2:1b

# 在聊天中輸入
>>> 你好，請介紹一下自己
>>> /bye  # 退出
```

## ✅ 安裝驗證

### 1. Python 環境驗證

```python
# test_setup.py
import sys
import pkg_resources

def check_python_version():
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 8):
        print("✅ Python 版本符合需求")
    else:
        print("❌ Python 版本過舊，請升級至 3.8+")

def check_packages():
    required_packages = [
        'langchain',
        'langchain-core',
        'python-dotenv',
    ]
    
    for package in required_packages:
        try:
            pkg_resources.get_distribution(package)
            print(f"✅ {package}: 已安裝")
        except pkg_resources.DistributionNotFound:
            print(f"❌ {package}: 未安裝")

if __name__ == "__main__":
    check_python_version()
    check_packages()
```

執行驗證：
```bash
python test_setup.py
```

### 2. LangChain 基本測試

```python
# test_langchain.py
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

def test_environment():
    """測試環境變數設定"""
    # 付費模型 API 金鑰
    paid_apis = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
    }
    
    # 免費模型 Token
    hf_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
    
    print("=== 付費模型金鑰狀態 ===")
    for key, value in paid_apis.items():
        if value:
            print(f"✅ {key}: 已設定")
        else:
            print(f"⚠️ {key}: 未設定（選用）")
    
    print("\n=== 免費模型Token狀態 ===")
    if hf_token:
        print("✅ HUGGINGFACEHUB_API_TOKEN: 已設定")
    else:
        print("ℹ️ HUGGINGFACEHUB_API_TOKEN: 未設定（選用）")

def test_langchain_import():
    """測試 LangChain 套件導入"""
    try:
        from langchain.prompts import PromptTemplate
        from langchain.schema import BaseOutputParser
        print("✅ LangChain 核心套件: 正常")
    except ImportError as e:
        print(f"❌ LangChain 導入失敗: {e}")

def test_ollama_connection():
    """測試 Ollama 連接"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print("✅ Ollama 服務: 運行中")
            models = response.json().get('models', [])
            print(f"   可用模型: {len(models)} 個")
        else:
            print("⚠️ Ollama 服務: 無回應")
    except Exception:
        print("⚠️ Ollama 服務: 未安裝或未啟動")

if __name__ == "__main__":
    print("=== LangChain 環境設置驗證 ===")
    test_environment()
    test_langchain_import() 
    test_ollama_connection()
    print("\n✅ 驗證完成！")
```

執行測試：
```bash
python test_langchain.py
```

## 🔧 開發工具設置

### 1. IDE 推薦

**VS Code 擴充功能:**
- Python
- Pylance
- Jupyter
- Python Docstring Generator
- GitLens

**PyCharm:**
- 專業的 Python IDE
- 內建虛擬環境管理
- 優秀的除錯功能

### 2. Jupyter Notebook

```bash
# 安裝 Jupyter
pip install jupyter notebook jupyterlab

# 啟動 Jupyter Lab
jupyter lab

# 或啟動 Notebook
jupyter notebook
```

### 3. Git 設置

```bash
# 初始化 Git 儲存庫
git init

# 創建 .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".venv/" >> .gitignore
echo "langchain-env/" >> .gitignore
```

## 🐛 常見問題解決

### 1. 套件安裝問題

**問題**: `pip install` 失敗
```bash
# 解決方案
pip install --upgrade pip
pip install --no-cache-dir package_name
```

**問題**: 權限錯誤
```bash
# 使用 --user 安裝
pip install --user package_name
```

### 2. 虛擬環境問題

**問題**: 無法啟動虛擬環境
```bash
# Windows PowerShell 執行政策
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 或直接使用
python -m venv langchain-env
```

### 3. API 連接問題

**問題**: API 金鑰無效
- 確認金鑰格式正確
- 檢查 `.env` 檔案位置
- 重新載入環境變數

**問題**: 網路連接失敗
- 檢查防火牆設定
- 確認代理伺服器配置
- 使用 VPN 或更換網路

### 4. 記憶體不足

**問題**: 本地模型記憶體不足
```bash
# 使用更小的模型（推薦）
ollama pull llama3.2:1b

# 或使用量化模型
ollama pull llama3.1:8b-instruct-q4_0
```

## 📚 下一步

環境設置完成後，您可以：

1. **[免費 LLM 模型指南](/tutorials/free-llm-models)** - 學習使用免費模型
2. **[第一個應用](/tutorials/first-app)** - 建構第一個 LangChain 應用
3. **[Demo 展示](/demos/)** - 體驗互動式範例

## 🔗 相關資源

### 官方文檔
- [LangChain 安裝指南](https://python.langchain.com/docs/get_started/installation)
- [Python 虛擬環境指南](https://docs.python.org/3/tutorial/venv.html)
- [Ollama 官方文檔](https://ollama.com)

### 社群資源
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [Python 套件索引](https://pypi.org/)
- [Hugging Face Hub](https://huggingface.co/)

---

::: tip 提示
完整的環境設置可能需要 20-30 分鐘，請耐心等待。如果遇到問題，請參考故障排除章節或查看官方文檔。
:::
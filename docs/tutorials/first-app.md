# 第一個 LangChain 應用

歡迎來到 LangChain 的實際應用教學！在這個章節中，我們將建構一個**智能角色問答助手**，展示 LangChain 的核心價值：將複雜的 AI 互動簡化為易於理解和維護的程式碼。

## 🚀 學習目標

完成本教學後，您將學會：

- 🔗 **LangChain 核心概念**：理解 LLM、Prompt Templates 和 Chains 的整合
- 🤖 **本地模型整合**：使用 Ollama 建構免費的 AI 應用
- 🎭 **角色扮演系統**：實作可切換角色的智能助手
- 🛠️ **錯誤處理**：建立穩健的應用程式
- 🧪 **測試和除錯**：確保程式碼品質

## 📋 先決條件

在開始之前，請確保您已經：

- ✅ 閱讀 [LangChain 介紹](/tutorials/introduction)
- ✅ 完成 [環境設置](/tutorials/setup)
- ✅ 安裝並熟悉 [免費 LLM 模型指南](/tutorials/free-llm-models)
- ✅ Ollama 正在運行，並已下載 `llama3.2:1b` 模型

::: tip 快速檢查
在終端執行 `ollama list` 確認您有可用的模型。如果沒有，請執行：
```bash
ollama pull llama3.2:1b
```
:::

## 🎯 我們要建構什麼？

我們將建構一個**智能角色問答助手**，特色包括：

- 🎭 **多重角色**：程式老師、翻譯員、生活顧問等
- 💬 **自然對話**：使用 LangChain 的 Prompt Templates
- 🏠 **本地運行**：完全免費，保護隱私
- 🔧 **易於擴展**：為後續教學（記憶、RAG等）奠定基礎

## 📦 環境準備

### 1. 創建專案目錄

```bash
mkdir my-first-langchain-app
cd my-first-langchain-app
```

### 2. 創建虛擬環境

```bash
# 創建虛擬環境
python -m venv venv

# 啟動虛擬環境
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### 3. 安裝必要套件

```bash
# 基礎 LangChain 套件
pip install langchain-ollama langchain-core

# Streamlit（用於 Web 介面）
pip install streamlit
```

### 4. 安裝和設置 Ollama

::: warning 重要步驟
如果您還未安裝 Ollama，請先完成此步驟。
:::

**安裝 Ollama:**

### Linux/Ubuntu
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### WSL2 (推薦)
```bash
# 1. 更新套件管理器
sudo apt update

# 2. 下載並安裝 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 3. 將 Ollama 添加到系統路徑（如果需要）
export PATH=$PATH:/usr/local/bin

# 4. 驗證安裝
ollama --version
```

::: tip WSL2 特別注意
如果遇到權限問題，可能需要：
```bash
# 重新載入 shell 配置
source ~/.bashrc

# 或重新啟動 WSL2
# 在 Windows PowerShell 中執行：wsl --shutdown
# 然後重新開啟 WSL2
```
:::

### macOS
```bash
# 使用 Homebrew
brew install ollama

# 或下載安裝程式
# 前往 https://ollama.com/download
```

### Windows
```powershell
# 前往 https://ollama.com/download 下載安裝程式
# 執行 .exe 檔案進行安裝

# 或使用 PowerShell (管理員權限)
winget install Ollama.Ollama
```

**啟動 Ollama 服務:**

### Linux/WSL2
```bash
# 方法 1: 前台啟動（開發測試用）
ollama serve

# 方法 2: 背景啟動（建議）
nohup ollama serve > ollama.log 2>&1 &

# 檢查服務狀態
ps aux | grep ollama
```

::: warning WSL2 常見問題
如果在 WSL2 中遇到啟動問題：

**問題 1: 服務無法啟動**
```bash
# 檢查是否有端口佔用
sudo netstat -tulpn | grep 11434

# 殺死佔用的進程
sudo pkill -f ollama
```

**問題 2: 權限問題**
```bash
# 確保用戶有執行權限
sudo chmod +x $(which ollama)

# 或重新安裝
curl -fsSL https://ollama.com/install.sh | sh
```

**問題 3: 路徑問題**
```bash
# 確認 Ollama 已安裝
which ollama

# 如果找不到，添加到 PATH
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc
```
:::

### macOS
```bash
# 啟動服務
ollama serve

# 或使用 brew services
brew services start ollama
```

### Windows
```powershell
# Windows 通常會自動啟動服務
# 如需手動啟動，在命令提示字元中執行：
ollama serve
```

**下載 llama3.2:1b 模型:**

```bash
# 下載模型（首次使用需要下載，約 1.3GB）
ollama pull llama3.2:1b

# 驗證模型已下載
ollama list
```

::: tip WSL2 下載注意事項
在 WSL2 中下載模型時：

**網路問題排除:**
```bash
# 如果下載緩慢或失敗，可以設定代理（如果有）
export https_proxy=http://proxy:port
export http_proxy=http://proxy:port

# 檢查網路連接
curl -I https://ollama.com
```

**儲存空間檢查:**
```bash
# 檢查可用空間（模型需要約 5GB）
df -h

# 檢查 Ollama 模型存放位置
ls -la ~/.ollama/models/
```

**下載進度監控:**
```bash
# 在另一個終端監控下載進度
watch -n 2 "du -sh ~/.ollama/models/"
```
:::

::: tip 模型選擇
如果您的電腦記憶體較小，可以選擇較小的模型：
- `llama3.2:1b` - 約 1.3GB，適合 4GB RAM（推薦教學使用）
- `llama3.2:3b` - 約 2GB，適合 8GB RAM  
- `llama3.1:8b` - 約 4.7GB，適合 16GB+ RAM
:::

### 5. 驗證 Ollama 連接

創建 `test_ollama.py` 來測試連接：

```python
from langchain_ollama import OllamaLLM

def test_ollama_connection():
    try:
        llm = OllamaLLM(model="llama3.2:1b")
        response = llm.invoke("Hello, 請用繁體中文回答：你是誰？")
        print("✅ Ollama 連接成功！")
        print(f"回應：{response}")
        return True
    except Exception as e:
        print(f"❌ Ollama 連接失敗：{e}")
        return False

if __name__ == "__main__":
    test_ollama_connection()
```

執行測試：
```bash
python test_ollama.py
```

## 🏗️ 步驟一：基礎 LLM 調用

讓我們從最簡單的 LLM 調用開始：

```python
# basic_llm.py
from langchain_ollama import OllamaLLM

def basic_llm_example():
    # 初始化 Ollama LLM
    llm = OllamaLLM(model="llama3.2:1b")
    
    # 簡單調用
    response = llm.invoke("請用繁體中文解釋什麼是人工智慧")
    print(response)

if __name__ == "__main__":
    basic_llm_example()
```

這個範例展示了最基本的 LLM 使用方式，但還不算是真正的 LangChain 應用。

## 🎨 步驟二：加入 Prompt Template

現在讓我們使用 LangChain 的 Prompt Template 來增加彈性：

```python
# prompt_template_example.py
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

def prompt_template_example():
    # 初始化 LLM
    llm = OllamaLLM(model="llama3.2:1b")
    
    # 創建 Prompt Template
    template = PromptTemplate.from_template(
        """你是一個{role}。請{task}：

問題：{question}

請用繁體中文回答，並且{style}。"""
    )
    
    # 使用模板生成 prompt
    prompt = template.format(
        role="Python 程式設計老師",
        task="用簡單易懂的方式解釋",
        question="什麼是函數？",
        style="包含實際的程式碼範例"
    )
    
    print("📝 生成的 Prompt：")
    print(prompt)
    print("\n" + "="*50 + "\n")
    
    # 調用 LLM
    response = llm.invoke(prompt)
    print("🤖 AI 回應：")
    print(response)

if __name__ == "__main__":
    prompt_template_example()
```

## ⛓️ 步驟三：建構 LangChain 鏈

這是 LangChain 的核心威力 - 將組件鏈接起來：

```python
# langchain_chain_example.py
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

def langchain_chain_example():
    # 初始化組件
    llm = OllamaLLM(model="llama3.2:1b")
    
    # 創建 Prompt Template
    template = PromptTemplate.from_template(
        """你是一個{role}。請{task}：

問題：{question}

請用繁體中文回答，並且{style}。"""
    )
    
    # 🔗 建構 LangChain 鏈
    chain = template | llm
    
    # 使用鏈
    response = chain.invoke({
        "role": "歷史老師",
        "task": "詳細說明",
        "question": "秦始皇統一中國的重要性",
        "style": "舉出具體的歷史事件和影響"
    })
    
    print("🔗 使用 LangChain 鏈的回應：")
    print(response)

if __name__ == "__main__":
    langchain_chain_example()
```

## 🎭 步驟四：完整的角色問答助手

現在讓我們建構完整的應用程式：

```python
# smart_assistant.py
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from typing import Dict, Any
import time

class SmartAssistant:
    def __init__(self, model_name: str = "llama3.2:1b"):
        """初始化智能助手"""
        self.llm = OllamaLLM(model=model_name)
        self.setup_templates()
        
    def setup_templates(self):
        """設置不同角色的模板"""
        self.templates = {
            "程式老師": PromptTemplate.from_template(
                """你是一個經驗豐富的程式設計老師。請用清楚易懂的方式回答學生的程式問題。

問題：{question}

請用繁體中文回答，並且：
1. 先解釋概念
2. 提供實際的程式碼範例
3. 指出常見的錯誤或注意事項
4. 建議進一步學習的方向"""
            ),
            
            "翻譯員": PromptTemplate.from_template(
                """你是一個專業的翻譯員。請協助翻譯以下內容。

要翻譯的內容：{question}

請提供：
1. 準確的翻譯
2. 文意說明（如果需要）
3. 使用情境（如果是俚語或專業術語）"""
            ),
            
            "生活顧問": PromptTemplate.from_template(
                """你是一個溫暖體貼的生活顧問。請針對使用者的生活問題提供建議。

問題：{question}

請用繁體中文回答，並且：
1. 表達同理心
2. 提供實用的建議
3. 分享相關的經驗或知識
4. 給予正面的鼓勵"""
            ),
            
            "學習夥伴": PromptTemplate.from_template(
                """你是一個友善的學習夥伴。請協助解答學習相關的問題。

問題：{question}

請用繁體中文回答，並且：
1. 分解複雜的概念
2. 提供記憶技巧或學習方法
3. 舉出實際的例子
4. 建議練習方式或資源"""
            )
        }
        
        # 建構鏈
        self.chains = {
            role: template | self.llm 
            for role, template in self.templates.items()
        }
    
    def get_available_roles(self) -> list:
        """取得可用角色列表"""
        return list(self.templates.keys())
    
    def ask(self, role: str, question: str) -> Dict[str, Any]:
        """向指定角色提問"""
        if role not in self.chains:
            return {
                "success": False,
                "error": f"角色 '{role}' 不存在。可用角色：{', '.join(self.get_available_roles())}"
            }
        
        try:
            # 記錄開始時間
            start_time = time.time()
            
            # 調用對應的鏈
            response = self.chains[role].invoke({"question": question})
            
            # 計算回應時間
            response_time = time.time() - start_time
            
            return {
                "success": True,
                "role": role,
                "question": question,
                "response": response,
                "response_time": f"{response_time:.2f}秒"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"發生錯誤：{str(e)}"
            }

def main():
    """主程式"""
    print("🎭 智能角色問答助手")
    print("=" * 40)
    
    # 初始化助手
    try:
        assistant = SmartAssistant()
        print("✅ 助手初始化成功！")
    except Exception as e:
        print(f"❌ 初始化失敗：{e}")
        return
    
    # 顯示可用角色
    roles = assistant.get_available_roles()
    print(f"\n📋 可用角色：{', '.join(roles)}")
    
    print("\n💡 使用說明：")
    print("- 輸入 'quit' 結束程式")
    print("- 輸入 'roles' 查看可用角色")
    print("- 格式：[角色] 您的問題")
    print("- 範例：程式老師 什麼是遞迴？")
    
    while True:
        print("\n" + "-" * 40)
        user_input = input("👤 請輸入（角色 問題）：").strip()
        
        # 處理特殊指令
        if user_input.lower() == 'quit':
            print("👋 再見！")
            break
        elif user_input.lower() == 'roles':
            print(f"📋 可用角色：{', '.join(roles)}")
            continue
        elif not user_input:
            print("❓ 請輸入問題")
            continue
        
        # 解析輸入
        parts = user_input.split(' ', 1)
        if len(parts) < 2:
            print("❓ 請使用格式：[角色] [問題]")
            continue
        
        role, question = parts[0], parts[1]
        
        # 提問
        print(f"\n🤔 向 {role} 提問：{question}")
        print("⏳ 思考中...")
        
        result = assistant.ask(role, question)
        
        if result["success"]:
            print(f"\n🎭 {result['role']} 的回答：")
            print("-" * 30)
            print(result["response"])
            print(f"\n⏱️  回應時間：{result['response_time']}")
        else:
            print(f"\n❌ 錯誤：{result['error']}")

if __name__ == "__main__":
    main()
```

## 🛠️ 步驟五：增強錯誤處理

讓我們為應用程式加入更完善的錯誤處理：

```python
# enhanced_assistant.py
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from typing import Dict, Any, Optional
import time
import logging
from pathlib import Path

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('assistant.log'),
        logging.StreamHandler()
    ]
)

class EnhancedSmartAssistant:
    def __init__(self, model_name: str = "llama3.2:1b", timeout: int = 60):
        """初始化增強版智能助手"""
        self.model_name = model_name
        self.timeout = timeout
        self.llm = None
        self.chains = {}
        
        # 初始化
        if not self._check_ollama_availability():
            raise ConnectionError("Ollama 服務不可用，請確認已安裝並啟動 Ollama")
        
        self._initialize_llm()
        self._setup_templates()
        
        logging.info(f"助手初始化完成，使用模型：{model_name}")
    
    def _check_ollama_availability(self) -> bool:
        """檢查 Ollama 是否可用"""
        try:
            import subprocess
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            logging.error(f"檢查 Ollama 可用性時發生錯誤：{e}")
            return False
    
    def _initialize_llm(self):
        """初始化 LLM"""
        try:
            self.llm = OllamaLLM(
                model=self.model_name,
                timeout=self.timeout
            )
            
            # 測試連接
            test_response = self.llm.invoke("Hello", timeout=10)
            logging.info("LLM 連接測試成功")
            
        except Exception as e:
            logging.error(f"LLM 初始化失敗：{e}")
            raise ConnectionError(f"無法初始化 LLM：{e}")
    
    def _setup_templates(self):
        """設置模板和鏈"""
        templates = {
            "程式老師": """你是一個經驗豐富的程式設計老師。請用清楚易懂的方式回答學生的程式問題。

問題：{question}

請用繁體中文回答，並且：
1. 先解釋概念
2. 提供實際的程式碼範例  
3. 指出常見的錯誤或注意事項
4. 建議進一步學習的方向""",

            "翻譯員": """你是一個專業的翻譯員。請協助翻譯以下內容。

要翻譯的內容：{question}

請提供：
1. 準確的翻譯
2. 文意說明（如果需要）
3. 使用情境（如果是俚語或專業術語）""",

            "生活顧問": """你是一個溫暖體貼的生活顧問。請針對使用者的生活問題提供建議。

問題：{question}

請用繁體中文回答，並且：
1. 表達同理心
2. 提供實用的建議
3. 分享相關的經驗或知識
4. 給予正面的鼓勵"""
        }
        
        try:
            self.chains = {}
            for role, template_str in templates.items():
                template = PromptTemplate.from_template(template_str)
                self.chains[role] = template | self.llm
                
            logging.info(f"成功設置 {len(self.chains)} 個角色")
            
        except Exception as e:
            logging.error(f"設置模板時發生錯誤：{e}")
            raise ValueError(f"模板設置失敗：{e}")
    
    def get_available_roles(self) -> list:
        """取得可用角色列表"""
        return list(self.chains.keys())
    
    def ask(self, role: str, question: str) -> Dict[str, Any]:
        """向指定角色提問（含錯誤處理）"""
        # 輸入驗證
        if not role or not question:
            return {
                "success": False,
                "error": "角色和問題都不能為空"
            }
        
        if role not in self.chains:
            return {
                "success": False,
                "error": f"角色 '{role}' 不存在。可用角色：{', '.join(self.get_available_roles())}"
            }
        
        # 問題長度檢查
        if len(question) > 1000:
            return {
                "success": False,
                "error": "問題過長，請控制在1000字以內"
            }
        
        try:
            logging.info(f"處理問題 - 角色：{role}，問題長度：{len(question)}")
            start_time = time.time()
            
            # 調用鏈
            response = self.chains[role].invoke(
                {"question": question.strip()},
                config={"timeout": self.timeout}
            )
            
            response_time = time.time() - start_time
            
            # 回應驗證
            if not response or len(response.strip()) == 0:
                return {
                    "success": False,
                    "error": "模型回應為空，請重試"
                }
            
            result = {
                "success": True,
                "role": role,
                "question": question,
                "response": response.strip(),
                "response_time": f"{response_time:.2f}秒",
                "model": self.model_name
            }
            
            logging.info(f"成功處理問題，回應時間：{response_time:.2f}秒")
            return result
            
        except TimeoutError:
            error_msg = f"請求超時（{self.timeout}秒），請重試"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
            
        except ConnectionError as e:
            error_msg = f"連接錯誤：{str(e)}"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
            
        except Exception as e:
            error_msg = f"未預期的錯誤：{str(e)}"
            logging.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def health_check(self) -> Dict[str, Any]:
        """健康檢查"""
        try:
            start_time = time.time()
            test_response = self.llm.invoke("Hello", timeout=10)
            response_time = time.time() - start_time
            
            return {
                "status": "healthy",
                "model": self.model_name,
                "response_time": f"{response_time:.2f}秒",
                "available_roles": len(self.chains)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }

def main():
    """主程式（含錯誤處理）"""
    print("🎭 增強版智能角色問答助手")
    print("=" * 50)
    
    try:
        # 初始化助手
        print("⏳ 正在初始化助手...")
        assistant = EnhancedSmartAssistant()
        print("✅ 助手初始化成功！")
        
        # 健康檢查
        health = assistant.health_check()
        if health["status"] == "healthy":
            print(f"💚 系統狀態：正常（回應時間：{health['response_time']}）")
        else:
            print(f"❌ 系統狀態：異常 - {health['error']}")
            return
            
    except Exception as e:
        print(f"❌ 初始化失敗：{e}")
        print("\n🔧 請檢查：")
        print("1. Ollama 是否已安裝並啟動")
        print("2. 是否已下載 llama3.2:1b 模型（ollama pull llama3.2:1b）")
        print("3. 網路連接是否正常")
        return
    
    # 顯示使用說明
    roles = assistant.get_available_roles()
    print(f"\n📋 可用角色：{', '.join(roles)}")
    print(f"🤖 使用模型：{assistant.model_name}")
    
    print("\n💡 使用說明：")
    print("- 輸入 'quit' 結束程式")
    print("- 輸入 'roles' 查看可用角色") 
    print("- 輸入 'health' 檢查系統狀態")
    print("- 格式：[角色] 您的問題")
    print("- 範例：程式老師 什麼是遞迴？")
    
    while True:
        try:
            print("\n" + "-" * 50)
            user_input = input("👤 請輸入（角色 問題）：").strip()
            
            # 處理特殊指令
            if user_input.lower() == 'quit':
                print("👋 再見！")
                break
            elif user_input.lower() == 'roles':
                print(f"📋 可用角色：{', '.join(roles)}")
                continue
            elif user_input.lower() == 'health':
                health = assistant.health_check()
                print(f"💚 系統狀態：{health}")
                continue
            elif not user_input:
                print("❓ 請輸入問題")
                continue
            
            # 解析輸入
            parts = user_input.split(' ', 1)
            if len(parts) < 2:
                print("❓ 請使用格式：[角色] [問題]")
                print(f"   可用角色：{', '.join(roles)}")
                continue
            
            role, question = parts[0], parts[1]
            
            # 提問
            print(f"\n🤔 向 {role} 提問：{question}")
            print("⏳ 思考中...")
            
            result = assistant.ask(role, question)
            
            if result["success"]:
                print(f"\n🎭 {result['role']} 的回答：")
                print("-" * 40)
                print(result["response"])
                print(f"\n⏱️  回應時間：{result['response_time']}")
                print(f"🤖 模型：{result['model']}")
            else:
                print(f"\n❌ 錯誤：{result['error']}")
                
        except KeyboardInterrupt:
            print("\n\n👋 程式已中斷，再見！")
            break
        except Exception as e:
            print(f"\n❌ 未預期的錯誤：{e}")
            logging.error(f"主程式錯誤：{e}")

if __name__ == "__main__":
    main()
```

## 🌐 步驟六：Streamlit Web 介面

讓我們為助手建立一個友善的 Web 介面：

```python
# streamlit_assistant.py
import streamlit as st
from enhanced_assistant import EnhancedSmartAssistant
import time
import logging

# 設置頁面
st.set_page_config(
    page_title="智能角色問答助手",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 session state
if 'assistant' not in st.session_state:
    st.session_state.assistant = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_role' not in st.session_state:
    st.session_state.current_role = "程式老師"

def initialize_assistant():
    """初始化助手"""
    try:
        with st.spinner('正在初始化助手...'):
            assistant = EnhancedSmartAssistant()
            return assistant
    except Exception as e:
        st.error(f"初始化失敗：{e}")
        st.info("請確認：\n1. Ollama 已安裝並啟動\n2. 已下載 llama3.1 模型\n3. 網路連接正常")
        return None

def main():
    """主應用程式"""
    # 標題
    st.title("🎭 智能角色問答助手")
    st.markdown("---")
    
    # 側邊欄
    with st.sidebar:
        st.header("⚙️ 設定")
        
        # 初始化按鈕
        if st.button("🚀 初始化助手", type="primary"):
            st.session_state.assistant = initialize_assistant()
        
        # 顯示系統狀態
        if st.session_state.assistant:
            with st.expander("💚 系統狀態", expanded=True):
                health = st.session_state.assistant.health_check()
                if health["status"] == "healthy":
                    st.success(f"✅ 正常運行\n回應時間：{health['response_time']}")
                    st.info(f"🤖 模型：{health.get('model', 'N/A')}\n角色數量：{health.get('available_roles', 0)}")
                else:
                    st.error(f"❌ 異常狀態\n錯誤：{health.get('error', 'Unknown')}")
            
            # 角色選擇
            st.markdown("### 🎭 選擇角色")
            roles = st.session_state.assistant.get_available_roles()
            st.session_state.current_role = st.selectbox(
                "請選擇要對話的角色：",
                roles,
                index=roles.index(st.session_state.current_role) if st.session_state.current_role in roles else 0
            )
            
            # 角色說明
            role_descriptions = {
                "程式老師": "💻 專精程式設計教學，提供清楚的概念解釋和程式碼範例",
                "翻譯員": "🌍 專業翻譯服務，提供準確翻譯和文化背景說明",
                "生活顧問": "💡 溫暖的生活建議，提供實用的解決方案和正面鼓勵"
            }
            
            if st.session_state.current_role in role_descriptions:
                st.info(role_descriptions[st.session_state.current_role])
            
            # 清除對話歷史
            if st.button("🗑️ 清除對話歷史"):
                st.session_state.chat_history = []
                st.rerun()
        
        else:
            st.warning("⚠️ 請先初始化助手")
    
    # 主要內容區域
    if st.session_state.assistant:
        # 對話區域
        st.header(f"💬 與 {st.session_state.current_role} 對話")
        
        # 顯示對話歷史
        chat_container = st.container()
        with chat_container:
            for i, chat in enumerate(st.session_state.chat_history):
                # 用戶問題
                with st.chat_message("user"):
                    st.write(f"**[{chat['role']}]** {chat['question']}")
                
                # AI 回應
                with st.chat_message("assistant"):
                    st.write(chat['response'])
                    
                    # 顯示詳細資訊
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.caption(f"⏱️ {chat['response_time']}")
                    with col2:
                        st.caption(f"🤖 {chat.get('model', 'N/A')}")
                    with col3:
                        st.caption(f"📅 {chat.get('timestamp', '')}")
        
        # 輸入區域
        st.markdown("### 💭 請輸入您的問題")
        
        with st.form("question_form", clear_on_submit=True):
            question = st.text_area(
                "問題內容：",
                placeholder=f"請向 {st.session_state.current_role} 提問...",
                help="輸入您想要詢問的問題，最多 1000 字",
                max_chars=1000
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                submit_button = st.form_submit_button("🚀 提問", type="primary")
            with col2:
                if st.form_submit_button("💡 範例問題"):
                    example_questions = {
                        "程式老師": ["什麼是遞迴？", "如何使用迴圈？", "解釋物件導向程式設計"],
                        "翻譯員": ["Hello World", "翻譯這句話：The quick brown fox", "What does 'serendipity' mean?"],
                        "生活顧問": ["如何管理時間？", "怎麼提高工作效率？", "如何處理壓力？"]
                    }
                    
                    examples = example_questions.get(st.session_state.current_role, [])
                    if examples:
                        st.info(f"💡 {st.session_state.current_role} 範例問題：\n" + "\n".join([f"• {q}" for q in examples]))
        
        # 處理提問
        if submit_button and question.strip():
            with st.spinner(f'🤔 {st.session_state.current_role} 正在思考中...'):
                result = st.session_state.assistant.ask(st.session_state.current_role, question)
                
                if result["success"]:
                    # 添加到對話歷史
                    chat_entry = {
                        "role": result["role"],
                        "question": result["question"],
                        "response": result["response"],
                        "response_time": result["response_time"],
                        "model": result.get("model", "N/A"),
                        "timestamp": time.strftime("%H:%M:%S")
                    }
                    st.session_state.chat_history.append(chat_entry)
                    
                    # 成功提示
                    st.success(f"✅ {result['role']} 已回答！回應時間：{result['response_time']}")
                    
                    # 重新運行以更新對話顯示
                    st.rerun()
                else:
                    st.error(f"❌ 錯誤：{result['error']}")
        
        elif submit_button and not question.strip():
            st.warning("⚠️ 請輸入問題內容")
        
        # 統計資訊
        if st.session_state.chat_history:
            st.markdown("---")
            with st.expander("📊 對話統計", expanded=False):
                total_questions = len(st.session_state.chat_history)
                role_stats = {}
                
                for chat in st.session_state.chat_history:
                    role = chat['role']
                    role_stats[role] = role_stats.get(role, 0) + 1
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("總問題數", total_questions)
                with col2:
                    avg_time = sum(float(chat['response_time'].replace('秒', '')) 
                                 for chat in st.session_state.chat_history) / total_questions
                    st.metric("平均回應時間", f"{avg_time:.2f}秒")
                
                st.markdown("**各角色使用次數：**")
                for role, count in role_stats.items():
                    st.write(f"• {role}: {count} 次")
    
    else:
        # 歡迎畫面
        st.markdown("""
        ## 👋 歡迎使用智能角色問答助手！
        
        這是一個基於 LangChain 和 Ollama 的 AI 助手，提供多種角色的專業服務：
        
        ### 🎭 可用角色
        - **💻 程式老師**：程式設計教學和技術問題解答
        - **🌍 翻譯員**：多語言翻譯和文化背景說明  
        - **💡 生活顧問**：生活建議和問題解決方案
        
        ### 🚀 開始使用
        1. 點擊左側的「🚀 初始化助手」按鈕
        2. 等待系統初始化完成
        3. 選擇您想對話的角色
        4. 開始提問！
        
        ### 💡 使用提示
        - 問題最多 1000 字
        - 可以隨時切換角色
        - 支援對話歷史記錄
        - 可以查看回應時間和統計資訊
        """)
        
        # 系統需求
        with st.expander("🔧 系統需求", expanded=False):
            st.markdown("""
            ### 必要條件
            - ✅ Python 3.8+
            - ✅ 已安裝 Ollama
            - ✅ 已下載 llama3.1 模型
            - ✅ 已安裝必要的 Python 套件
            
            ### 安裝指令
            ```bash
            # 安裝 LangChain 套件
            pip install langchain-ollama langchain-core streamlit
            
            # 安裝 Ollama
            curl -fsSL https://ollama.com/install.sh | sh
            
            # 下載模型（推薦教學使用）
            ollama pull llama3.2:1b
            
            # 啟動助手
            streamlit run streamlit_assistant.py
            ```
            """)

if __name__ == "__main__":
    main()
```

啟動 Streamlit 應用：

```bash
# 確保在虛擬環境中
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 啟動 Streamlit 應用
streamlit run streamlit_assistant.py
```

### 🎨 Streamlit 介面特色

**優勢：**
- 🖱️ **圖形化介面**：無需命令列操作
- 🔄 **即時互動**：所見即所得的對話體驗
- 📊 **統計資訊**：對話歷史和性能統計
- 🎭 **角色切換**：一鍵切換不同角色
- 📱 **響應式設計**：支援桌面和行動裝置

**功能亮點：**
- 側邊欄系統狀態監控
- 對話歷史保存和顯示
- 範例問題提示
- 回應時間和統計資訊
- 錯誤處理和用戶提示

## 🧪 測試和驗證

創建測試檔案來驗證我們的應用：

```python
# test_assistant.py
import unittest
from enhanced_assistant import EnhancedSmartAssistant
import time

class TestSmartAssistant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """測試類別初始化"""
        try:
            cls.assistant = EnhancedSmartAssistant()
        except Exception as e:
            raise unittest.SkipTest(f"無法初始化助手：{e}")
    
    def test_initialization(self):
        """測試初始化"""
        self.assertIsNotNone(self.assistant.llm)
        self.assertGreater(len(self.assistant.chains), 0)
    
    def test_available_roles(self):
        """測試角色列表"""
        roles = self.assistant.get_available_roles()
        self.assertIsInstance(roles, list)
        self.assertIn("程式老師", roles)
        self.assertIn("翻譯員", roles)
    
    def test_valid_question(self):
        """測試有效問題"""
        result = self.assistant.ask("程式老師", "什麼是變數？")
        self.assertTrue(result["success"])
        self.assertIn("response", result)
        self.assertGreater(len(result["response"]), 10)
    
    def test_invalid_role(self):
        """測試無效角色"""
        result = self.assistant.ask("無效角色", "測試問題")
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_empty_inputs(self):
        """測試空輸入"""
        result = self.assistant.ask("", "測試問題")
        self.assertFalse(result["success"])
        
        result = self.assistant.ask("程式老師", "")
        self.assertFalse(result["success"])
    
    def test_long_question(self):
        """測試過長問題"""
        long_question = "測試" * 500  # 1000+ 字符
        result = self.assistant.ask("程式老師", long_question)
        self.assertFalse(result["success"])
    
    def test_health_check(self):
        """測試健康檢查"""
        health = self.assistant.health_check()
        self.assertIn("status", health)

if __name__ == "__main__":
    # 執行測試
    unittest.main(verbosity=2)
```

## 📚 完整專案結構

您的專案目錄應該看起來像這樣：

```
my-first-langchain-app/
├── venv/                    # 虛擬環境
├── basic_llm.py            # 基礎 LLM 範例
├── prompt_template_example.py  # Prompt Template 範例
├── langchain_chain_example.py  # LangChain 鏈範例
├── smart_assistant.py      # 完整助手應用（命令列版）
├── enhanced_assistant.py   # 增強版助手（命令列版）
├── streamlit_assistant.py  # Streamlit Web 介面版本
├── test_assistant.py       # 測試檔案
├── test_ollama.py         # Ollama 連接測試
├── assistant.log          # 應用日誌
└── README.md              # 專案說明
```

## 🎯 總結

恭喜！您已經成功建構了第一個 LangChain 應用程式。在這個過程中，您學會了：

### 🔑 核心概念
- **LangChain 的價值**：將複雜的 AI 互動抽象化
- **組件化設計**：LLM + Prompt Template + Chain
- **本地模型整合**：使用 Ollama 的優勢

### 🛠️ 實用技能
- **錯誤處理**：網路連接、超時、輸入驗證
- **日誌記錄**：追蹤應用程式行為
- **測試驗證**：確保程式碼品質
- **用戶體驗**：友善的命令列介面和 Web 介面
- **介面設計**：使用 Streamlit 建構互動式 Web 應用

### 🚀 進階準備
這個應用為後續學習奠定了基礎：
- **記憶系統**：可以為助手加入對話記憶
- **RAG 整合**：可以讓助手查詢知識庫
- **工具調用**：可以讓助手執行實際任務
- **部署上線**：已有 Streamlit Web 介面，可進一步部署為雲端服務
- **多模態整合**：可加入圖片、語音等多媒體支援

## 🔗 下一步

建議您接下來學習：

1. **[Chat Models 對話模型](/tutorials/chat-models)** - 深入理解對話模型的原理
2. **[Prompt Template 提示範本](/tutorials/prompt-template)** - 學習更進階的提示設計
3. **[LCEL 表達式語言](/tutorials/lcel)** - 掌握 LangChain 的鏈式語法

## 🤝 參與討論

如果您在建構過程中遇到問題，或有改進建議，歡迎：

- 📝 在我們的 [GitHub Issues](https://github.com/your-repo/issues) 提出問題
- 💬 參與 [討論區](https://github.com/your-repo/discussions) 分享經驗
- 🌟 如果這個教學對您有幫助，請給我們一個 Star！

---

**🎉 您已經踏出了 LangChain 開發的第一步！**
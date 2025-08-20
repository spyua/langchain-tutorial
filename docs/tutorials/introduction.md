# LangChain 介紹

## 什麼是 LangChain？

LangChain 是一個多功能的框架，可以用來建立利用大型語言模型（LLMs）的應用程式，目前提供 Python 與 TypeScript 版本。

它的核心理念是：最有影響力、最具特色的應用，不應僅僅透過 API 與語言模型互動，而應該同時做到以下兩點：

### 🔍 增強資料感知（Enhance Data Awareness）

**核心概念：** 讓 LLM 不再是「閉門造車」，而是能主動感知、檢索並整合外部資料。

#### 為什麼需要資料感知？

想像一下這些情境：

📋 **傳統 LLM 的限制**：
- 問：「我們公司的請假政策是什麼？」
- 答：「我無法知道您公司的具體政策...」

🎯 **增強資料感知後**：
- 問：「我們公司的請假政策是什麼？」  
- 答：「根據公司手冊，員工每年享有14天年假，病假需要提前通知...」

#### 實際應用場景

**場景一：企業客服機器人**
- **問題**：客戶問訂單狀態，傳統 AI 無法查詢
- **解決**：接入訂單系統，即時查詢回答

**場景二：法務文件分析**  
- **問題**：需要從大量合約中找特定條款
- **解決**：掃描所有文件，精準定位相關內容

**場景三：個人健康助手**
- **問題**：AI 不知道你的健康紀錄
- **解決**：整合健康數據，提供個人化建議

#### 技術實現層級

| 層級 | 能力 | 實際例子 |
|------|------|---------|
| **靜態感知** | 預先載入的知識庫 | 公司FAQ、產品手冊問答 |
| **動態感知** | 實時資料檢索 | 股價查詢、天氣預報 |
| **上下文感知** | 對話歷史記憶 | 記住你的偏好和需求 |
| **環境感知** | 感知外部系統狀態 | 監控系統告警、IoT設備數據 |

#### 程式碼實現範例

::: details 點擊查看：檢索增強生成 (RAG) 實作
```python
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

# pip install -U langchain langchain-openai langchain-community langchain-chroma pypdf

# 載入外部文件
loader = PyPDFLoader("company_handbook.pdf")
documents = loader.load()

# 切分文件
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=150
)
splits = splitter.split_documents(documents)

# 建立向量資料庫（需要先定義 embeddings）
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(splits, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 建立文件整合鏈
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_template(
    "根據以下文件回覆：{context}\n問題：{input}"
)
stuff_chain = create_stuff_documents_chain(llm, prompt)

# 建立檢索增強生成鏈（新版 v0.2+ 做法）
rag_chain = create_retrieval_chain(retriever, stuff_chain)

# LLM 現在能回答文件中的內容
response = rag_chain.invoke({"input": "公司的請假政策是什麼？"})
print(response["answer"])
```
:::

::: details 點擊查看：動態資料注入實作
```python
from langchain.prompts import PromptTemplate
from datetime import datetime

# 感知當前時間資料
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

# 模擬數據函數（實際應用中需要實作）
def get_latest_market_data():
    return {"stock_price": 150.25, "volume": 1000000, "trend": "up"}

prompt = PromptTemplate.from_template(
    "現在時間是 {current_time}，根據當前時間和歷史資料 {historical_data} 來分析趨勢"
)

# LLM 能感知實時資料
formatted_prompt = prompt.format(
    current_time=current_time,
    historical_data=get_latest_market_data()
)
```
:::

::: details 點擊查看：多源資料整合實作
```python
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

# 讓 LLM 感知資料庫
db = SQLDatabase.from_uri("sqlite:///sales.db")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# LLM 能查詢資料庫並整合結果（新版 invoke 格式）
sql_agent = create_sql_agent(llm, db, verbose=True)
response = sql_agent.invoke({"input": "分析本月銷售趨勢並與去年同期比較"})
print(response["output"])

# 🔒 安全機制說明：
# 1. 輸入驗證：所有工具都應進行參數驗證
# 2. 權限控制：限制 Agent 能訪問的資源範圍
# 3. 超時設定：防止長時間執行造成資源消耗
# 4. 稽核機制：重要操作先由人類確認
# 5. 日誌記錄：記錄所有 Agent 操作供稽核
```
:::


### 🤖 增強行動力（Enhance Agency）

**核心概念：** 讓 LLM 從被動回答變成主動決策，能自主選擇工具、規劃步驟，並執行複雜任務。

#### 為什麼需要行動力？

想像一下你有一個真正的 AI 助手：

🤖 **傳統 LLM 的限制**：
- 你：「幫我安排明天的會議」
- AI：「我無法直接操作您的行事曆，建議您...」

⚡ **增強行動力後**：
- 你：「幫我安排明天的會議」  
- AI：「我已經檢查了您的行事曆，發現下午2點有空檔，已經發送會議邀請給相關人員，並預訂了會議室。」

#### 實際應用場景

**場景一：智能行政助手**
- **需求**：「幫我分析銷售報表並發給主管」
- **AI 行動**：
  1. 🔍 連接資料庫查詢銷售數據
  2. 📊 生成圖表和分析報告  
  3. 📧 自動發送郵件給指定主管

**場景二：客服問題解決**
- **客戶**：「我要退貨，但找不到訂單」
- **AI 行動**：
  1. 🔍 查詢客戶訂單記錄
  2. 📋 確認退貨政策適用性
  3. 🎫 自動生成退貨單並發送

**場景三：智能監控系統**
- **系統告警**：「伺服器 CPU 使用率 90%」
- **AI 行動**：
  1. 📊 分析歷史性能數據
  2. ⚖️ 自動調整負載平衡
  3. 📱 通知運維團隊並提供建議

#### 行動力的層級發展

| 層級 | 能力特徵 | 實際應用 |
|------|----------|----------|
| **反應式行動** | 根據指令執行單一動作 | 「幫我查天氣」→ 調用天氣 API |
| **計劃式行動** | 制定多步驟執行計劃 | 「安排出差」→ 訂機票+飯店+通知同事 |
| **自適應行動** | 根據結果調整策略 | 遇到問題時自動嘗試備選方案 |
| **創新式行動** | 創造性解決新問題 | 面對未知情況時設計新的解決流程 |

#### AI Agent 的思考過程

**範例：「幫我分析競爭對手並制定行銷策略」**

```
🤔 AI 思考：我需要先了解競爭對手情況
🔍 AI 行動：使用搜尋工具查找競爭對手資訊
👁️ AI 觀察：獲得競爭對手清單和特色

🤔 AI 思考：現在需要分析市場趨勢  
🔍 AI 行動：搜尋相關行業報告
👁️ AI 觀察：獲得市場數據和預測

🤔 AI 思考：結合資料制定策略
📝 AI 行動：整合分析並提出建議
✅ AI 完成：輸出完整的行銷策略報告
```

#### 程式碼實現範例

::: details 點擊查看：智能工具調用實作
```python
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import ast
import operator

# 安全計算器（只允許基本數學運算）
def safe_calculate(expression: str):
    """安全的數學計算器，避免使用 eval()"""
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg
    }
    
    def _eval(node):
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num):  # 向下相容
            return node.n
        elif isinstance(node, ast.BinOp):
            if type(node.op) in allowed_operators:
                return allowed_operators[type(node.op)](_eval(node.left), _eval(node.right))
            else:
                raise ValueError(f"不支援的運算子: {type(node.op).__name__}")
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) in allowed_operators:
                return allowed_operators[type(node.op)](_eval(node.operand))
            else:
                raise ValueError(f"不支援的一元運算子: {type(node.op).__name__}")
        else:
            raise ValueError(f"不支援的運算式: {type(node).__name__}")
    
    try:
        node = ast.parse(expression, mode='eval')
        return _eval(node.body)
    except Exception as e:
        return f"計算錯誤: {str(e)}"

def search_web(query):
    """模擬網路搜尋功能"""
    return f"搜尋結果: {query} - 相關內容已找到"

def send_email(recipient, content):
    """模擬郵件發送（Dry-run模式）"""
    return f"[乾執行] 郵件將發送給 {recipient}: {content[:50]}..."

# 安全的工具集
tools = [
    Tool(name="搜尋", func=search_web, description="搜尋網路資訊"),
    Tool(name="安全計算", func=safe_calculate, description="安全的數學計算（只允許 +, -, *, /, ** 運算）"),
    Tool(name="模擬發送郵件", func=send_email, description="模擬發送電子郵件（測試模式）")
]

# ❗️ 重要：工具調用相容性說明
# Tool Calling 需要支援此功能的模型：
# ✅ 支援：GPT-4, GPT-4o, Claude-3, Gemini Pro
# ❌ 不支援：部分開源模型、GPT-3.5-turbo 舊版本
# 若模型不支援 Tool Calling，將降級為一般文字生成
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 建立 prompt 模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一個有用的助手。使用提供的工具來完成任務。"),
    ("user", "{input}"),
    ("assistant", "{agent_scratchpad}"),
])

# LLM 能自主決定使用哪個工具
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 複雜任務自主分解與執行（正確的 invoke 格式）
response = agent_executor.invoke({
    "input": "幫我搜尋最新的AI發展趨勢，計算 (100+50)*2 的結果，然後模擬發送總結報告給經理"
})
print(response["output"])

# 🔒 安全機制說明：
# 1. 輸入驗證：所有工具都應進行參數驗證
# 2. 權限控制：限制 Agent 能訪問的資源範圍
# 3. 超時設定：防止長時間執行造成資源消耗
# 4. 稽核機制：重要操作先由人類確認
# 5. 日誌記錄：記錄所有 Agent 操作供稽核
```
:::

::: details 點擊查看：多步驟推理決策實作
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_openai import ChatOpenAI

# ReAct 代理：推理-行動-觀察循環（新版 v0.2+ 做法）
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 使用官方 ReAct prompt 模板
prompt = hub.pull("hwchase17/react")

# 建立 ReAct agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True,  # 處理解析錯誤
    max_iterations=5  # 限制最大迭代次數
)

# LLM 會自主進行多輪推理（正確的 invoke 格式）
result = agent_executor.invoke({
    "input": "我需要為新產品制定行銷策略。請搜尋競爭對手資訊、分析市場趨勢，並提出建議。"
})
print(result["output"])
```
:::

::: details 點擊查看：條件判斷流程控制實作
```python
# 此範例已更新為 v0.2+ 新版做法，使用 create_react_agent
# ConversationalAgent 已棄用，建議使用 RunnableWithMessageHistory

# 對話式代理（新版做法：使用 RunnableWithMessageHistory）
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# 記憶儲存
store = {}
def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 帶記憶的 Agent
conversational_agent = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="output",
)

# LLM 能根據條件與歷史執行不同行動
response = conversational_agent.invoke(
    {"input": "如果今天股價上漲超過5%，就模擬發送慶祝郵件；否則分析下跌原因"},
    config={"configurable": {"session_id": "trading_session"}}
)
print(response["output"])
```
:::


#### 實際應用案例

**智能客服系統：**
```python
# 客服代理能感知客戶資料並自主決定行動（更新為 v0.2+ 新版）
# 首先定義客服工具
from langchain.tools import Tool

def get_customer_info(customer_id: str):
    """查詢客戶資訊（模擬）"""
    return f"客戶 {customer_id}: VIP會員，註冊日期 2023-01-15"

def check_order_status(order_id: str):
    """查詢訂單狀態（模擬）"""
    return f"訂單 {order_id}: 已出貨，預計 2024-01-20 送達"

def process_refund(order_id: str, reason: str):
    """處理退款（模擬）"""
    return f"[模擬] 訂單 {order_id} 退款申請已提交，原因: {reason}"

def escalate_to_human(issue: str):
    """轉人工客服（模擬）"""
    return f"[模擬] 已轉交人工客服處理: {issue}"

customer_tools = [
    Tool(name="查詢客戶資訊", func=get_customer_info, description="查詢客戶基本資訊"),
    Tool(name="查詢訂單狀態", func=check_order_status, description="查詢訂單物流狀態"),
    Tool(name="處理退款", func=process_refund, description="處理退款申請"),
    Tool(name="轉人工客服", func=escalate_to_human, description="複雜問題轉人工處理")
]

customer_service_agent = AgentExecutor(
    agent=create_tool_calling_agent(llm, customer_tools, prompt),
    tools=customer_tools,
    verbose=True
)

# 自主處理複雜客服情境（正確的 invoke 格式）
response = customer_service_agent.invoke({
    "input": "客戶抱怨商品有問題要退貨，客戶ID是C001，訂單編號是O12345，請幫我處理"
})
print(response["output"])

# 🔒 安全機制說明：
# 1. 輸入驗證：所有工具都應進行參數驗證
# 2. 權限控制：限制 Agent 能訪問的資源範圍
# 3. 超時設定：防止長時間執行造成資源消耗
# 4. 稽核機制：重要操作先由人類確認
# 5. 日誌記錄：記錄所有 Agent 操作供稽核
```

**智能分析師：**
```python
# 分析代理能整合多源資料並自主產出報告（更新為 v0.2+ 新版）
def query_database(query: str):
    """查詢資料庫（模擬）"""
    return f"資料庫查詢結果: {query} - 找到 150 筆記錄"

def fetch_market_data(period: str):
    """獲取市場資料（模擬）"""
    return f"{period} 市場資料: 成長 15%, 競爭激烈度中等"

def generate_charts(data_type: str):
    """生成圖表（模擬）"""
    return f"[模擬] {data_type} 圖表已生成，儲存至 charts/{data_type}.png"

def create_presentation(content: str):
    """製作簡報（模擬）"""
    return f"[模擬] 簡報已生成: {content[:100]}..."

analyst_tools = [
    Tool(name="查詢資料庫", func=query_database, description="查詢內部業務資料庫"),
    Tool(name="獲取市場資料", func=fetch_market_data, description="獲取外部市場資訊"),
    Tool(name="生成圖表", func=generate_charts, description="生成資料視覺化圖表"),
    Tool(name="製作簡報", func=create_presentation, description="製作分析簡報")
]

analyst_agent = AgentExecutor(
    agent=create_tool_calling_agent(llm, analyst_tools, prompt),
    tools=analyst_tools,
    verbose=True
)

# 自主完成完整分析流程（正確的 invoke 格式）
report = analyst_agent.invoke({
    "input": "製作本季度業績分析報告，包含趨勢分析和改善建議"
})
print(report["output"])
```

#### 🔒 安全開發原則

在開發 LangChain 應用時，安全性應是第一優先考量：

| 安全面向 | 具體做法 | 實作範例 |
|------------|----------|---------|
| **輸入驗證** | 所有工具都要檢查參數合法性 | `assert isinstance(amount, (int, float)) and amount > 0` |
| **權限控制** | 限制 Agent 可訪問的資源範圍 | 白名單、資料庫角色分離 |
| **超時機制** | 防止工具無限期執行 | `timeout=30` 參數設定 |
| **人工稽核** | 重要操作需人類確認 | 轉帳、刪除數據等操作 |
| **日誌追蹤** | 記錄所有 Agent 行為 | LangSmith 整合、本地日誌 |
| **率限控制** | 防止 API 濫用 | 每分鐘/每小時調用次數限制 |

### 📝 產業級開發建議

1. **不要在生產環境使用** `eval()`、`exec()` 等危險函數
2. **始終使用環境變數** 來儲存 API 金鑰，勿硬編碼
3. **實作断路器模式** 讓使用者能隨時終止 Agent 運行
4. **設計失效安全機制** 當工具失效時，應有合理的備用方案
5. **定期安全稽核** 查看 Agent 行為記錄，發現異常行為

## 總結：資料感知 + 行動力 = 智能應用

**傳統 LLM：** 只能根據訓練資料回答問題
**LangChain 增強後：** 
- 🔍 **感知外部世界**：即時資料、文件、資料庫
- 🤖 **主動採取行動**：調用工具、執行任務、做決策
- 🔄 **持續學習適應**：根據結果調整策略

這就是 LangChain 讓 LLM 從「聊天機器人」進化成「智能助手」的關鍵所在。

---

::: tip 下一步
現在你已經了解 LangChain 的基本概念，接下來可以：
1. [LangChain 架構與核心概念](/tutorials/architecture) - 深入了解架構與抽象化
2. [環境設置](/tutorials/setup) - 準備開發環境
3. [免費 LLM 模型指南](/tutorials/free-llm-models) - 了解免費模型選項
4. [第一個應用](/tutorials/first-app) - 動手實作
:::

::: warning 版本相容性提醒
本文檔已更新至 **LangChain v0.2+ 標準**，但框架仍在快速發展中：

- ✅ **已更新**：`create_retrieval_chain`、`create_react_agent`、LCEL 管道語法
- ⚠️ **棄用中**：`RetrievalQA`、`initialize_agent`、`ConversationalRetrievalChain`
- 🆕 **新特性**：LangGraph、更強的 Output Parsers、LangSmith 整合

建議此順序查看最新資訊：
1. [官方文檔](https://python.langchain.com/) - 最新 API 參考
2. [LangGraph 文檔](https://langchain-ai.github.io/langgraph/) - 新一代 Agent 框架
3. [LangSmith](https://smith.langchain.com/) - 可觀測性與調試工具
:::
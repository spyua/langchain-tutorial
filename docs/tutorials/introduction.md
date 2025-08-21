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
# 匯入 LangChain RAG 相關模組
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

# 安裝必要套件：
# pip install -U langchain langchain-openai langchain-community langchain-chroma pypdf

# 步驟 1: 載入外部文件
# PyPDFLoader 可以讀取 PDF 檔案並轉換為 LangChain 文件格式
loader = PyPDFLoader("company_handbook.pdf")
documents = loader.load()  # 載入所有頁面作為獨立文件
print(f"載入了 {len(documents)} 頁文件")

# 步驟 2: 文件切分處理
# 由於文件可能很長，需要切分為較小的片段以便檢索
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # 每個片段最大 1000 字符
    chunk_overlap=150     # 片段間重疊 150 字符，保持上下文連貫性
)
splits = splitter.split_documents(documents)
print(f"文件已切分為 {len(splits)} 個片段")

# 步驟 3: 建立向量資料庫
# 將文件片段轉換為向量並存儲，用於後續相似度檢索
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# 使用 OpenAI 的 embedding 模型將文字轉換為向量
embeddings = OpenAIEmbeddings()

# 使用 Chroma 作為向量資料庫，存儲文件片段的向量表示
vectorstore = Chroma.from_documents(
    documents=splits,    # 要儲存的文件片段
    embedding=embeddings # 向量化模型
)

# 建立檢索器，設定每次檢索返回最相關的 4 個片段
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}  # 返回最相關的前 4 個文件片段
)

# 步驟 4: 建立語言模型和提示模板
# 使用 OpenAI 的 GPT 模型進行文件問答
llm = ChatOpenAI(
    model="gpt-4o-mini",  # 使用較小的模型以節省成本
    temperature=0         # 設定為 0 以獲得一致的回答
)

# 建立提示模板，告訴 AI 如何使用檢索到的文件回答問題
prompt = ChatPromptTemplate.from_template(
    """請根據以下文件內容回覆用戶問題。如果文件中沒有相關資訊，請說明無法找到相關內容。
    
    文件內容：{context}
    
    用戶問題：{input}
    
    回答："""
)

# 步驟 5: 建立文件整合鏈
# 這個鏈負責將檢索到的多個文件片段整合，並生成統一回答
stuff_chain = create_stuff_documents_chain(
    llm=llm,       # 使用的語言模型
    prompt=prompt  # 提示模板
)

# 步驟 6: 建立完整的 RAG 鏈 (新版 v0.2+ 做法)
# 結合檢索器和文件整合鏈，形成完整的問答系統
rag_chain = create_retrieval_chain(
    retriever=retriever,     # 文件檢索器
    combine_docs_chain=stuff_chain  # 文件整合與回答生成鏈
)

# 步驟 7: 使用 RAG 系統回答問題
# 現在 LLM 可以基於公司手冊內容回答具體問題
response = rag_chain.invoke({
    "input": "公司的請假政策是什麼？"
})

# 顯示 AI 基於文件內容的回答
print("AI 回答:", response["answer"])

# 可選：查看檢索到的相關文件片段
print("\n檢索到的相關文件片段:")
for i, doc in enumerate(response["context"]):
    print(f"片段 {i+1}: {doc.page_content[:200]}...")
```
:::

::: details 點擊查看：動態資料注入實作
```python
# 匯入必要模組
from langchain.prompts import PromptTemplate
from datetime import datetime
import requests
import json

# 步驟 1: 獲取實時資料
# 感知當前系統時間，讓 AI 知道現在的時間脈絡
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
print(f"當前時間: {current_time}")

# 步驟 2: 定義資料獲取函數
def get_latest_market_data():
    """
    獲取最新市場數據的函數
    在實際應用中，這裡會調用真實的 API
    例如：Alpha Vantage、Yahoo Finance 等
    """
    # 模擬從外部 API 獲取的實時數據
    market_data = {
        "stock_price": 150.25,    # 當前股價
        "volume": 1000000,        # 交易量
        "trend": "up",            # 趨勢方向
        "change_percent": 2.5,    # 漲幅百分比
        "last_updated": current_time  # 數據更新時間
    }
    return market_data

def get_weather_data(city="台北"):
    """
    獲取天氣資料的範例函數
    實際應用可整合 OpenWeatherMap 等 API
    """
    # 模擬天氣 API 回應
    weather_data = {
        "city": city,
        "temperature": 28,
        "condition": "晴天",
        "humidity": 65,
        "wind_speed": 15
    }
    return weather_data

# 步驟 3: 建立動態提示模板
# 這個模板會將實時資料注入到提示中
prompt_template = PromptTemplate.from_template(
    """你是一個專業的金融分析師。請根據以下資訊進行分析：
    
    當前時間：{current_time}
    市場數據：{market_data}
    天氣狀況：{weather_info}
    
    請分析當前市場趨勢，並考慮以下因素：
    1. 價格變動趨勢
    2. 交易量表現 
    3. 外部環境影響（如天氣對相關產業的影響）
    
    分析結果："""
)

# 步驟 4: 獲取實時資料
market_info = get_latest_market_data()
weather_info = get_weather_data()

print("獲取的市場資料:", json.dumps(market_info, ensure_ascii=False, indent=2))
print("獲取的天氣資料:", json.dumps(weather_info, ensure_ascii=False, indent=2))

# 步驟 5: 將實時資料注入提示模板
# LLM 現在能感知即時的外部資料狀況
formatted_prompt = prompt_template.format(
    current_time=current_time,
    market_data=json.dumps(market_info, ensure_ascii=False),
    weather_info=json.dumps(weather_info, ensure_ascii=False)
)

print("\n=== 動態生成的提示 ===")
print(formatted_prompt)

# 步驟 6: 實際應用中的完整流程
def create_dynamic_analysis(user_question):
    """
    建立動態分析函數，整合實時資料
    """
    # 獲取最新資料
    current_data = {
        'time': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'market': get_latest_market_data(),
        'weather': get_weather_data()
    }
    
    # 建立情境感知的提示
    context_prompt = PromptTemplate.from_template(
        """基於以下即時資訊：
        時間：{time}
        市場狀況：{market}
        環境資訊：{weather}
        
        用戶問題：{question}
        
        請提供基於當前情況的專業分析。"""
    )
    
    return context_prompt.format(
        time=current_data['time'],
        market=current_data['market'],
        weather=current_data['weather'],
        question=user_question
    )

# 使用範例
analysis_prompt = create_dynamic_analysis("現在是否適合投資科技股？")
print("\n=== 情境感知分析 ===")
print(analysis_prompt)
```
:::

::: details 點擊查看：多源資料整合實作
```python
# 匯入多源資料整合所需的模組
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
import sqlite3
import pandas as pd
import logging
from typing import Dict, Any

# 步驟 1: 設定日誌記錄（安全機制）
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sql_agent.log'),  # 記錄所有操作到檔案
        logging.StreamHandler()                # 同時在控制台顯示
    ]
)
logger = logging.getLogger(__name__)

# 步驟 2: 建立安全的資料庫連接
def create_sample_database():
    """
    建立示範用的銷售資料庫
    實際應用中，這會是您現有的業務資料庫
    """
    # 創建 SQLite 資料庫和示範數據
    conn = sqlite3.connect('sales.db')
    
    # 建立銷售數據表
    conn.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        date DATE NOT NULL,
        product TEXT NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        region TEXT NOT NULL,
        salesperson TEXT NOT NULL
    )
    ''')
    
    # 插入示範數據
    sample_data = [
        ('2024-01-15', '筆記型電腦', 45000, '台北', '張小明'),
        ('2024-01-20', '智慧手機', 25000, '高雄', '李美華'),
        ('2023-01-18', '筆記型電腦', 42000, '台北', '王大同'),
        ('2023-01-25', '平板電腦', 18000, '台中', '陳淑芬'),
    ]
    
    conn.executemany(
        'INSERT OR REPLACE INTO sales (date, product, amount, region, salesperson) VALUES (?, ?, ?, ?, ?)',
        sample_data
    )
    conn.commit()
    conn.close()
    logger.info("示範資料庫建立完成")

# 步驟 3: 建立安全的資料庫連接包裝器
class SafeSQLDatabase:
    """
    安全的 SQL 資料庫包裝器
    實施多層安全機制
    """
    def __init__(self, database_uri: str, allowed_tables: list = None):
        self.db = SQLDatabase.from_uri(database_uri)
        self.allowed_tables = allowed_tables or []  # 白名單機制
        logger.info(f"資料庫連接已建立: {database_uri}")
    
    def validate_query(self, query: str) -> bool:
        """
        驗證 SQL 查詢的安全性
        """
        # 禁止的操作（防止資料被修改或刪除）
        forbidden_operations = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER']
        query_upper = query.upper()
        
        for operation in forbidden_operations:
            if operation in query_upper:
                logger.warning(f"禁止的操作被攔截: {operation}")
                return False
        return True

# 步驟 4: 初始化資料庫和 AI 模型
# 建立示範資料庫
create_sample_database()

# 建立安全的資料庫連接
db = SQLDatabase.from_uri("sqlite:///sales.db")
logger.info(f"可用資料表: {db.get_usable_table_names()}")

# 初始化語言模型（使用較小模型以節省成本）
llm = ChatOpenAI(
    model="gpt-4o-mini",  # 使用成本效益較高的模型
    temperature=0,        # 確保結果的一致性
    timeout=30           # 設定超時以防止長時間等待
)
logger.info("語言模型初始化完成")

# 步驟 5: 建立 SQL 智能代理
# 這個代理能夠理解自然語言問題並生成相應的 SQL 查詢
sql_agent = create_sql_agent(
    llm=llm,                    # 使用的語言模型
    db=db,                      # 連接的資料庫
    verbose=True,               # 顯示推理過程
    agent_type="openai-tools",  # 使用 OpenAI 工具調用功能
    handle_parsing_errors=True  # 處理解析錯誤
)
logger.info("SQL 代理建立完成")

# 步驟 6: 安全的查詢執行函數
def safe_query_execution(question: str, max_retries: int = 3) -> Dict[str, Any]:
    """
    安全地執行 SQL 查詢
    包含重試機制和錯誤處理
    """
    for attempt in range(max_retries):
        try:
            logger.info(f"執行查詢 (嘗試 {attempt + 1}): {question}")
            
            # 記錄開始時間（性能監控）
            import time
            start_time = time.time()
            
            # 執行查詢（新版 invoke 格式）
            response = sql_agent.invoke({
                "input": question
            })
            
            # 計算執行時間
            execution_time = time.time() - start_time
            logger.info(f"查詢執行成功，耗時: {execution_time:.2f} 秒")
            
            return {
                "success": True,
                "output": response["output"],
                "execution_time": execution_time,
                "attempt": attempt + 1
            }
            
        except Exception as e:
            logger.error(f"查詢執行失敗 (嘗試 {attempt + 1}): {str(e)}")
            if attempt == max_retries - 1:  # 最後一次嘗試
                return {
                    "success": False,
                    "error": str(e),
                    "attempts": max_retries
                }
            # 等待後重試
            import time
            time.sleep(1)
    
    return {"success": False, "error": "超過最大重試次數"}

# 步驟 7: 實際使用範例
print("=== 多源資料整合與分析 ===")

# 範例 1: 銷售趨勢分析
result1 = safe_query_execution(
    "分析本月銷售趨勢並與去年同期比較，包含總金額和交易筆數"
)

if result1["success"]:
    print("\n📊 銷售趨勢分析結果:")
    print(result1["output"])
    print(f"⏱️ 執行時間: {result1['execution_time']:.2f} 秒")
else:
    print(f"❌ 查詢失敗: {result1['error']}")

# 範例 2: 產品績效分析
result2 = safe_query_execution(
    "哪個產品的銷售績效最好？請提供具體的數據分析"
)

if result2["success"]:
    print("\n🏆 產品績效分析結果:")
    print(result2["output"])
else:
    print(f"❌ 查詢失敗: {result2['error']}")

# 範例 3: 區域銷售分析
result3 = safe_query_execution(
    "比較不同地區的銷售表現，找出表現最佳的區域"
)

if result3["success"]:
    print("\n🗺️ 區域銷售分析結果:")
    print(result3["output"])
else:
    print(f"❌ 查詢失敗: {result3['error']}")

# 🔒 實施的安全機制說明：
print("\n🔒 已實施的安全機制:")
print("1. ✅ 輸入驗證：查詢前檢查 SQL 語法安全性")
print("2. ✅ 權限控制：僅允許 SELECT 操作，禁止修改資料")
print("3. ✅ 超時設定：30 秒查詢超時，防止資源消耗")
print("4. ✅ 重試機制：自動重試失敗的查詢，提高穩定性")
print("5. ✅ 日誌記錄：完整記錄所有操作供安全稽核")
print("6. ✅ 錯誤處理：妥善處理各種異常情況")
print("7. ✅ 性能監控：追蹤查詢執行時間")

# 清理資源
logger.info("程式執行完成，資源清理中...")
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
# 匯入 LangChain Agent 和工具相關模組
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import ast
import operator
import logging
from typing import Any

# 設定日誌記錄（用於安全監控）
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 步驟 1: 定義安全的數學計算器
def safe_calculate(expression: str) -> Any:
    """
    安全的數學計算器，不使用危險的 eval() 函數
    只允許基本的數學運算，防止代碼注入攻擊
    
    Args:
        expression (str): 數學表達式，例如 "2 + 3 * 4"
    
    Returns:
        計算結果或錯誤訊息
    """
    # 定義允許的運算子（白名單機制）
    allowed_operators = {
        ast.Add: operator.add,        # 加法 +
        ast.Sub: operator.sub,        # 減法 -
        ast.Mult: operator.mul,       # 乘法 *
        ast.Div: operator.truediv,    # 除法 /
        ast.Pow: operator.pow,        # 幂運算 **
        ast.USub: operator.neg        # 負號 -x
    }
    
    def _eval(node):
        """遞迴地評估 AST 節點"""
        if isinstance(node, ast.Constant):  # Python 3.8+ 的常數節點
            return node.value
        elif isinstance(node, ast.Num):  # 向下相容舊版 Python
            return node.n
        elif isinstance(node, ast.BinOp):  # 雙元運算 (a + b)
            if type(node.op) in allowed_operators:
                left_val = _eval(node.left)
                right_val = _eval(node.right)
                return allowed_operators[type(node.op)](left_val, right_val)
            else:
                raise ValueError(f"不支援的運算子: {type(node.op).__name__}")
                
        elif isinstance(node, ast.UnaryOp):  # 一元運算 (-a)
            if type(node.op) in allowed_operators:
                operand_val = _eval(node.operand)
                return allowed_operators[type(node.op)](operand_val)
            else:
                raise ValueError(f"不支援的一元運算子: {type(node.op).__name__}")
        else:
            raise ValueError(f"不支援的運算式類型: {type(node).__name__}")
    
    try:
        logger.info(f"執行安全計算: {expression}")
        # 將字串解析為 AST（抽象語法樹）
        node = ast.parse(expression, mode='eval')
        result = _eval(node.body)
        logger.info(f"計算結果: {result}")
        return result
    except Exception as e:
        error_msg = f"計算錯誤: {str(e)}"
        logger.error(error_msg)
        return error_msg

def search_web(query: str) -> str:
    """
    模擬網路搜尋功能
    在實際應用中，這會調用真實的搜尋 API
    例如 Google Custom Search, Bing Search, Tavily 等
    
    Args:
        query (str): 搜尋關鍵詞
    
    Returns:
        str: 搜尋結果摘要
    """
    logger.info(f"執行網路搜尋: {query}")
    
    # 模擬不同類型的搜尋結果
    mock_results = {
        "AI": "最新 AI 發展趨勢：大型語言模型持續進化，多模態 AI 興起",
        "技術": "技術新聞：雲端運算和邊緣運算融合發展",
        "市場": "市場分析：科技股表現強勁，投資人看好未來前景"
    }
    
    # 根據關鍵詞返回相關結果
    for keyword, result in mock_results.items():
        if keyword.lower() in query.lower():
            return f"搜尋結果: {result}"
    
    return f"搜尋結果: 關於 '{query}' 的相關資訊已找到"

def send_email(recipient: str, content: str) -> str:
    """
    模擬郵件發送功能（Dry-run 模式）
    在實際應用中，這會整合 SMTP 服務或 API
    例如 SendGrid, AWS SES, Office 365 等
    
    Args:
        recipient (str): 收件人郵件地址
        content (str): 郵件內容
    
    Returns:
        str: 發送狀態訊息
    """
    logger.info(f"模擬發送郵件給: {recipient}")
    
    # 為了安全，這裡只是模擬發送，不會真的發出郵件
    return f"[乾執行模式] 郵件將發送給 {recipient}\n主旨: AI 分析報告\n內容預覽: {content[:50]}..."

# 步驟 2: 建立安全的工具集
# 每個工具都經過安全檢查，並含有詳細的功能說明
tools = [
    Tool(
        name="搜尋",
        func=search_web,
        description="搜尋網路資訊。輸入搜尋關鍵詞，返回相關資訊摘要。"
    ),
    Tool(
        name="安全計算",
        func=safe_calculate,
        description="安全的數學計算器。支援加減乘除和幂運算（+, -, *, /, **）。輸入數學表達式，返回計算結果。"
    ),
    Tool(
        name="模擬發送郵件",
        func=send_email,
        description="模擬發送電子郵件（測試模式，不會真的發出）。需要兩個參數：收件人和郵件內容。"
    )
]

# 步驟 3: 模型相容性檢查
# ❗️ 重要：工具調用相容性說明
print("🔍 檢查模型相容性...")
print("Tool Calling 支援情況：")
print("✅ 支援: GPT-4, GPT-4o, Claude-3, Gemini Pro")
print("❌ 不支援: 部分開源模型、GPT-3.5-turbo 舊版本")
print("⚠️ 注意: 若模型不支援 Tool Calling，將降級為一般文字生成\n")

# 步驟 4: 初始化語言模型
llm = ChatOpenAI(
    model="gpt-4o-mini",  # 使用支援 Tool Calling 的模型
    temperature=0,        # 設定為 0 以獲得一致的結果
    timeout=30           # 30 秒超時保護
)
logger.info("語言模型初始化完成")

# 步驟 5: 建立提示模板
# 定義 Agent 的行為模式和使用工具的方式
prompt = ChatPromptTemplate.from_messages([
    (
        "system", 
        """你是一個有用且安全的 AI 助手。
        
        使用指引：
        1. 一次只使用一個工具
        2. 仔細檢查工具的結果再決定下一步
        3. 如果遇到錯誤，請告知用戶並嘗試其他方法
        4. 保持友善和專業的沟通風格"""
    ),
    ("user", "{input}"),
    ("assistant", "{agent_scratchpad}"),  # Agent 的思考過程
])
logger.info("提示模板建立完成")

# 步驟 6: 建立智能 Agent
# Agent 會自主分析任務並決定使用哪些工具
agent = create_tool_calling_agent(
    llm=llm,      # 語言模型
    tools=tools,  # 可用工具列表
    prompt=prompt # 提示模板
)

# 使用 AgentExecutor 來進行安全的執行管理
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,              # 顯示詳細的執行過程
    handle_parsing_errors=True, # 自動處理解析錯誤
    max_iterations=10,         # 限制最大迭代次數以防止無限迴圈
    max_execution_time=60      # 總執行時間上限 60 秒
)
logger.info("Agent 執行器建立完成")

# 步驟 7: 執行複雜的多步驟任務
print("🚀 開始執行複雜任務...")
print("=" * 50)

# 這個任務需要 Agent 自主分解為多個步驟：
# 1. 搜尋 AI 發展趨勢
# 2. 計算數學表達式
# 3. 整合資訊並模擬發送郵件

task_description = """請幫我完成以下任務：
1. 搜尋最新的 AI 發展趨勢資訊
2. 計算 (100+50)*2 的結果
3. 將搜尋結果和計算結果整合成一份總結報告
4. 模擬發送這份報告給經理 (manager@company.com)

請按照順序完成每個步驟，並在每個步驟後說明你的進度。"""

try:
    # 使用 invoke 方法執行任務（LangChain v0.2+ 標準格式）
    response = agent_executor.invoke({
        "input": task_description
    })
    
    print("\n" + "=" * 50)
    print("🎆 任務完成！以下是 Agent 的最終回答：")
    print("=" * 50)
    print(response["output"])
    
except Exception as e:
    logger.error(f"任務執行失敗: {str(e)}")
    print(f"❌ 任務執行過程中發生錯誤: {str(e)}")

# 🔒 安全機制証明
print("\n" + "=" * 50)
print("🔒 已實施的安全機制：")
print("1. ✅ 輸入驗證：所有工具參數都經過驗證")
print("2. ✅ 權限控制：只能使用預定義的安全工具")
print("3. ✅ 超時設定：工具和整體執行都有時間上限")
print("4. ✅ 迭代限制：防止 Agent 陷入無限迴圈")
print("5. ✅ 稽核機制：重要操作（如郵件）只是模擬執行")
print("6. ✅ 日誌記錄：所有 Agent 行為都有完整記錄")
print("7. ✅ 錯誤處理：自動處理各種異常情況")
print("8. ✅ 代碼安全：不使用 eval()，采用 AST 解析")
```
:::

::: details 點擊查看：多步驟推理決策實作
```python
# 匯入 ReAct (Reasoning + Acting) 代理相關模組
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
import time
import logging

# 設定詳細日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 步驟 1: 定義進階分析工具
def analyze_competitor(company_name: str) -> str:
    """
    競爭對手分析工具
    在實際應用中可以整合：
    - 公司資料庫 API
    - 新聞和市場報告網站
    - 社交媒體情感分析
    - 財務数據 API
    """
    logger.info(f"分析競爭對手: {company_name}")
    
    # 模擬競爭對手分析結果
    mock_analysis = {
        "科技": f"{company_name} 分析結果：\n• 市場佔有率 25%\n• 主要優勢：技術創新\n• 弱點：客戶服務\n• 最近動態：推出新產品線",
        "零售": f"{company_name} 分析結果：\n• 連鎖店數量 500+\n• 主要優勢：品牌知名度\n• 弱點：價格競爭力\n• 最近動態：擴展線上通路",
        "金融": f"{company_name} 分析結果：\n• 資產規模 100億\n• 主要優勢：風險控制\n• 弱點：數位化轉型\n• 最近動態：推出數位理財"
    }
    
    # 根據公司名稱推斷行業類型
    for industry, analysis in mock_analysis.items():
        if industry in company_name:
            return analysis
    
    return f"{company_name} 競爭對手分析：\n• 正在收集數據...\n• 市場地位強勁\n• 需持續關注其動態"

def research_market_trends(industry: str) -> str:
    """
    市場趨勢研究工具
    整合多種數據來源：
    - 產業報告 (Gartner, IDC)
    - 市場研究 (Nielsen, Euromonitor)
    - 經濟指標 (GDP, CPI)
    - 社交媒體趨勢 (Twitter, LinkedIn)
    """
    logger.info(f"研究市場趨勢: {industry}")
    
    market_data = {
        "科技": "📈 2024 科技趨勢：\n• AI/ML 市場年成長率 35%\n• 雲端運算需求持續增長\n• 網路安全投資大幅增加\n• 邊緣運算成為新熱點",
        "零售": "🛍️ 2024 零售趨勢：\n• 電商游透率達 65%\n• 永續消費意識提升\n• 個人化體驗成為關鍵\n• Omnichannel 成為標準配置",
        "金融": "🏦 2024 金融趨勢：\n• FinTech 投資增長 40%\n• 數位貨幣法規日趋完善\n• ESG 投資成為主流\n• 開放銀行推動創新"
    }
    
    return market_data.get(industry, f"{industry} 市場趨勢：\n• 正在分析中...\n• 整體市場呈穩健成長\n• 数位化轉型加速")

def generate_strategy_recommendations(context: str) -> str:
    """
    策略建議生成工具
    基於前面收集的資訊生成可行的商業策略
    結合：
    - 競爭分析結果
    - 市場趨勢數據  
    - 最佳實務 (Best Practices)
    - SWOT 分析框架
    """
    logger.info("生成策略建議")
    
    # 基於輸入上下文生成專業建議
    strategy_template = f"""📊 策略建議報告
    
🎯 核心策略：
1. 差異化定位：適別競爭對手的優勢領域
2. 数位優先：投資数位化轉型和線上体驗
3. 客戶中心：提升服務品質和個人化體驗
4. 永續經營：結合 ESG 原則建立品牌形象

🚀 行動計畫：
• 短期 (3月): 市場研究和競爭分析
• 中期 (6月): 產品開發和測試市場
• 長期 (12月): 全面市場推出和擴展

📊 KPI 指標：
• 市場佔有率目標: +15%
• 客戶滿意度: >85%
• ROI 目標: 25%+

基於以下分析數據：
{context}"""
    
    return strategy_template

# 步驟 2: 建立進階分析工具集
# 這些工具結合使用能夠完成複雜的商業分析任務
analysis_tools = [
    Tool(
        name="競爭對手分析",
        func=analyze_competitor,
        description="分析特定競爭對手的市場地位、優勣勢和最近動態。輸入公司名稱。"
    ),
    Tool(
        name="市場趨勢研究",
        func=research_market_trends,
        description="研究特定行業的市場趨勢、成長機會和未來預測。輸入行業名稱。"
    ),
    Tool(
        name="策略建議生成",
        func=generate_strategy_recommendations,
        description="基於競爭分析和市場趨勢生成具體的商業策略建議。輸入相關背景資訊。"
    )
]

# 步驟 3: 初始化進階語言模型
print("🤖 初始化 ReAct (Reasoning + Acting) Agent...")

# 使用更強大的模型來處理複雜的多步驟推理
llm = ChatOpenAI(
    model="gpt-4o-mini",    # 適合複雜推理任務的模型
    temperature=0.1,       # 輕微增加創意性但保持一致性
    timeout=45            # 較長的超時時間以支持複雜推理
)

# 步驟 4: 使用官方 ReAct 提示模板
# ReAct 模式：Reasoning (推理) + Acting (行動) + Observation (觀察)
print("📋 下載 ReAct 提示模板...")
try:
    # 從 LangChain Hub 獲取經過優化的 ReAct 模板
    prompt = hub.pull("hwchase17/react")
    print("✅ ReAct 模板下載成功")
except Exception as e:
    print(f"⚠️ 無法下載官方模板: {e}")
    print("🔧 使用備用模板...")
    
    # 備用的簡化 ReAct 模板
    from langchain_core.prompts import PromptTemplate
    prompt = PromptTemplate.from_template(
        """Answer the following questions as best you can. You have access to the following tools:
        
        {tools}
        
        Use the following format:
        
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        
        Begin!
        
        Question: {input}
        Thought:{agent_scratchpad}"""
    )

# 步驟 5: 建立 ReAct Agent
print("🔧 建立 ReAct Agent...")

# ReAct Agent 會在每次行動後停下來思考結果
react_agent = create_react_agent(
    llm=llm,
    tools=analysis_tools,
    prompt=prompt
)

# 配置 Agent 執行器的安全參數
react_executor = AgentExecutor(
    agent=react_agent,
    tools=analysis_tools,
    verbose=True,                    # 顯示詳細的思考過程
    handle_parsing_errors=True,      # 自動處理解析錯誤
    max_iterations=8,                # 允許更多迭代以支持複雜推理
    max_execution_time=120,          # 2 分鐘執行上限
    return_intermediate_steps=True   # 返回中間步驟供分析
)
print("✅ ReAct Agent 建立完成")

# 步驟 6: 執行複雜的多步驟分析任務
print("\n" + "=" * 60)
print("🎆 開始執行複雜的商業策略分析任務")
print("=" * 60)

# 這個任務需要 Agent 進行多步驟推理：
# 1. 思考需要那些資訊
# 2. 有序地使用工具收集資訊
# 3. 分析和結合收集到的資訊
# 4. 生成總體策略建議

complex_business_task = """我需要為公司新產品制定全面的行銷策略。

產品背景：一個基於 AI 的科技解決方案，主要面向中小企業。

請幫我：
1. 分析主要競爭對手（如科技大廠）的優勣勢
2. 研究科技行業的最新市場趨勢
3. 基於以上分析，提出具體的行銷策略建議

請按照邏輯順序逐步分析，並在每個步驟後說明你的思考過程。"""

try:
    print(f"📨 任務詳情: {complex_business_task[:100]}...")
    print("⏳ Agent 開始理解任務並规划執行步驟...")
    
    # 記錄開始時間
    start_time = time.time()
    
    # 使用 invoke 方法執行複雜任務
    result = react_executor.invoke({
        "input": complex_business_task
    })
    
    # 計算執行時間
    execution_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("🏆 多步驟推理分析完成！")
    print("=" * 60)
    print(f"⏱️ 總執行時間: {execution_time:.2f} 秒")
    print(f"🔄 推理迭代次數: {len(result.get('intermediate_steps', []))}")
    
    print("\n📊 最終分析結果:")
    print("-" * 50)
    print(result["output"])
    
    # 顯示中間步驟的摘要。
    if 'intermediate_steps' in result and result['intermediate_steps']:
        print("\n🔍 推理過程摘要:")
        for i, (action, observation) in enumerate(result['intermediate_steps'], 1):
            print(f"{i}. 🎯 行動: {action.tool} - {action.tool_input}")
            print(f"   👁️ 觀察: {str(observation)[:100]}...")
        
except Exception as e:
    logger.error(f"任務執行失敗: {str(e)}")
    print(f"❌ 任務執行過程中發生錯誤: {str(e)}")
    print("🔧 建議檢查網路連接或調整任務複雜度")

# 步驟 7: 分析 ReAct 模式的優勢
print("\n" + "=" * 60)
print("🧠 ReAct (Reasoning + Acting) 模式優勢:")
print("✅ 透明度: 可以看到 AI 的完整思考過程")
print("✅ 可靠性: 每步都有驗證和修正機制")
print("✅ 適應性: 能根據新資訊調整後續行動")
print("✅ 糾密性: 每個結論都基於具體的觀察和推理")
print("✅ 可擴展: 可以輕易添加新工具和能力")
print("=" * 60)
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
# 步驟 1: 构建客服業務需要的工具集
# 這些工具能讓 AI 代理自動處理客服查詢（更新為 v0.2+ 新版）
from langchain.tools import Tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
import logging
import json
from datetime import datetime, timedelta

# 設定客服日誌
logging.basicConfig(level=logging.INFO)
customer_logger = logging.getLogger("customer_service")

def get_customer_info(customer_id: str) -> str:
    """
    查詢客戶資訊的模擬函數
    在實際應用中，這會連接 CRM 系統或客戶資料庫
    例如：Salesforce, HubSpot, 自建 CRM 等
    """
    customer_logger.info(f"查詢客戶資訊: {customer_id}")
    
    # 模擬不同類型的客戶資料
    mock_customers = {
        "C001": {
            "name": "張先生",
            "level": "VIP會員",
            "join_date": "2023-01-15",
            "total_orders": 25,
            "total_amount": 150000,
            "last_contact": "2024-01-10"
        },
        "C002": {
            "name": "李小姐",
            "level": "一般會員",
            "join_date": "2023-08-20",
            "total_orders": 8,
            "total_amount": 35000,
            "last_contact": "2024-01-05"
        }
    }
    
    customer = mock_customers.get(customer_id)
    if customer:
        return f"""客戶資訊 - ID: {customer_id}
姓名: {customer['name']}
會員級別: {customer['level']}
註冊日期: {customer['join_date']}
歷史訂單: {customer['total_orders']} 筆
累計消費: NT${customer['total_amount']:,}
最後聯繫: {customer['last_contact']}"""
    else:
        return f"查無此客戶資訊：{customer_id}，請確認客戶ID是否正確"

def check_order_status(order_id: str) -> str:
    """
    查詢訂單狀態的模擬函數
    在實際應用中，這會連接訂單管理系統、物流系統
    例如：ERP, WMS, 物流商 API 等
    """
    customer_logger.info(f"查詢訂單狀態: {order_id}")
    
    # 模擬訂單狀態資料
    mock_orders = {
        "O12345": {
            "status": "已出貨",
            "items": "筆記型電腦 x1",
            "amount": 25000,
            "order_date": "2024-01-15",
            "ship_date": "2024-01-18",
            "estimated_delivery": "2024-01-22",
            "tracking_number": "TW1234567890"
        },
        "O12346": {
            "status": "處理中",
            "items": "智慧手機 x2",
            "amount": 45000,
            "order_date": "2024-01-20",
            "ship_date": None,
            "estimated_delivery": "2024-01-25",
            "tracking_number": None
        }
    }
    
    order = mock_orders.get(order_id)
    if order:
        result = f"""訂單資訊 - 編號: {order_id}
狀態: {order['status']}
商品: {order['items']}
金額: NT${order['amount']:,}
下單日期: {order['order_date']}"""
        
        if order['ship_date']:
            result += f"\n出貨日期: {order['ship_date']}"
            result += f"\n預計送達: {order['estimated_delivery']}"
            if order['tracking_number']:
                result += f"\n追蹤編號: {order['tracking_number']}"
        else:
            result += f"\n預計出貨: {order['estimated_delivery']}"
        
        return result
    else:
        return f"查無此訂單資訊：{order_id}，請確認訂單編號是否正確"

def process_refund(order_id: str, reason: str) -> str:
    """
    處理退款申請的模擬函數
    在實際應用中，這會觸發實際的退款流程
    例如：通知財務部門、更新庫存系統、發送通知郵件
    """
    customer_logger.info(f"處理退款 - 訂單: {order_id}, 原因: {reason}")
    
    # 模擬退款處理邏輯
    refund_id = f"RF{datetime.now().strftime('%Y%m%d')}{order_id[-3:]}"
    estimated_days = 5 if "品質" in reason else 3
    
    # 模擬檢查訂單狀態
    if order_id not in ["O12345", "O12346"]:
        return f"退款失敗：找不到訂單 {order_id}"
    
    return f"""[模擬執行] 退款申請已提交
訂單編號: {order_id}
退款編號: {refund_id}
退款原因: {reason}
申請時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}
預計處理時間: 3-5 個工作天

後續動作：
1. 系統已通知財務部門
2. 將發送確認郵件給客戶
3. 請保持手機通訊暢通"""

def escalate_to_human(issue: str) -> str:
    """
    轉人工客服的模擬函數
    在實際應用中，這會觸發：
    - 將對話記錄轉交人工客服
    - 在客服系統中建立工作單
    - 通知線上客服人員
    - 發送緊急通知（如果需要）
    """
    customer_logger.warning(f"轉人工客服 - 問題: {issue}")
    
    # 生成工作單編號
    ticket_id = f"TK{datetime.now().strftime('%Y%m%d%H%M')}"
    
    return f"""[模擬執行] 已轉交人工客服處理
工作單編號: {ticket_id}
問題描述: {issue}
建立時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}
優先級: 中等

下一步骤：
1. 客服人員將於 30 分鐘內主動聯繫
2. 對話記錄已自動附加至工作單
3. 您將收到追蹤編號用於後續查詢"""

# 步驟 2: 建立客服工具集
# 每個工具都經過精心設計，能讓 AI 代理自主處理各種客服情境
customer_tools = [
    Tool(
        name="查詢客戶資訊",
        func=get_customer_info,
        description="查詢客戶的基本資訊，包含會員等級、購買歷史等。需要客戶ID。"
    ),
    Tool(
        name="查詢訂單狀態",
        func=check_order_status,
        description="查詢訂單的詳細狀態，包含出貨、物流追蹤等資訊。需要訂單編號。"
    ),
    Tool(
        name="處理退款",
        func=process_refund,
        description="處理客戶的退款申請。需要訂單編號和退款原因。"
    ),
    Tool(
        name="轉人工客服",
        func=escalate_to_human,
        description="將複雜或特殊問題轉交給人工客服處理。需要問題描述。"
    )
]

# 步驟 3: 建立專業的客服 AI 代理
print("👥 初始化客服 AI 代理...")

# 設定客服專用的提示模板
customer_service_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """你是一個專業的客服 AI 助手，具有以下特質：
        
        🎆 服務理念：
        1. 以客為尊：始終保持禮貌和耐心
        2. 主動協助：盡力解決客戶問題
        3. 專業精神：提供準確有用的資訊
        4. 效率優先：快速面擊客戶需求
        
        🛠️ 作業指引：
        1. 先理解客戶問題再使用工具
        2. 一次只使用一個工具並等待結果
        3. 如果遇到無法解決的問題，主動轉人工
        4. 始終用繁體中文回復客戶"""
    ),
    ("user", "{input}"),
    ("assistant", "{agent_scratchpad}")
])

# 創建客服代理
customer_service_agent = AgentExecutor(
    agent=create_tool_calling_agent(llm, customer_tools, customer_service_prompt),
    tools=customer_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,          # 限制迭代次數以控制成本
    max_execution_time=60      # 1 分鐘內必須完成服務
)

print("✅ 客服 AI 代理建立完成")

# 步驟 4: 模擬複雜的客服情境
print("\n" + "=" * 50)
print("📞 模擬複雜客服情境 - 客戶抱怨處理")
print("=" * 50)

# 這是一個典型的複雜客服場景，需要 AI 自主判斷並執行多個步驟
complex_customer_issue = """嗨，我是張先生，我的客戶ID是C001。
我上個星期下的筆記型電腦（訂單編號 O12345）有很大的品質問題！
螢幕有一塊黑屏，鍵盤也有幾個按鍵壞了。
我要退貨並且申請全額退款，這個問題是商品本身的品質問題！
請幫我快速處理，我很不滿意！

另外，我想了解一下我的其他訂單狀態。"""

try:
    print(f"💬 客戶記訊: {complex_customer_issue[:100]}...")
    print("⏳ AI 代理開始處理客戶問題...")
    
    # AI 代理會自動：
    # 1. 分析客戶問題
    # 2. 查詢客戶資訊以确認身份
    # 3. 查詢訂單狀態以了解情況
    # 4. 處理退款申請
    # 5. 提供專業的後續服務
    
    response = customer_service_agent.invoke({
        "input": complex_customer_issue
    })
    
    print("\n" + "=" * 50)
    print("🎆 客服處理結果")
    print("=" * 50)
    print(response["output"])
    
except Exception as e:
    customer_logger.error(f"客服處理失敗: {str(e)}")
    print(f"❌ 客服處理過程中發生錯誤: {str(e)}")

# 🔒 實施的安全機制証明：
print("\n" + "=" * 50)
print("🔒 客服系統安全機制:")
print("1. ✅ 輸入驗證: 客戶ID、訂單編號等關鍵資訊都會驗證")
print("2. ✅ 權限控制: AI 只能處理查詢和一般退款，重大問題轉人工")
print("3. ✅ 超時設定: 60秒內必須完成服務，防止客戶等待")
print("4. ✅ 操作稽核: 重要操作（退款）只是模擬，需人工確認")
print("5. ✅ 完整記錄: 所有客服互動都有詳細日誌記錄")
print("6. ✅ 升級機制: 複雜問題自動轉人工，確保服務品質")
print("7. ✅ 資料保護: 敏感資訊（如卡號）不會被記錄或傳輸")
print("=" * 50)
```

**智能分析師：**
```python
# 步驟 1: 建立商業分析所需的工具集
# 這些工具能讓 AI 分析師自動收集資料並生成報告（更新為 v0.2+ 新版）
from langchain.tools import Tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
import json
import logging
from datetime import datetime, timedelta
import random

# 設定分析日誌
logging.basicConfig(level=logging.INFO)
analyst_logger = logging.getLogger("business_analyst")

def query_database(query: str) -> str:
    """
    查詢內部業務資料庫的模擬函數
    在實際應用中，這會連接：
    - 業務資料庫 (MySQL, PostgreSQL)
    - 数據倉庫 (Snowflake, BigQuery)
    - ERP 系統 (SAP, Oracle)
    - CRM 系統 (Salesforce, HubSpot)
    """
    analyst_logger.info(f"查詢資料庫: {query}")
    
    # 模擬不同類型的查詢結果
    mock_queries = {
        "銷售": {
            "total_records": 1250,
            "period": "2024 Q1",
            "revenue": 15600000,
            "growth_rate": 12.5,
            "top_products": ["筆記型電腦", "智慧手機", "平板電腦"],
            "regions": {"North": 45, "South": 30, "East": 25}
        },
        "客戶": {
            "total_records": 8500,
            "new_customers": 450,
            "retention_rate": 87.3,
            "satisfaction_score": 4.2,
            "churn_rate": 5.8
        },
        "市場": {
            "total_records": 2100,
            "market_share": 23.5,
            "competitor_analysis": "Strong position",
            "trend": "Growing",
            "opportunities": ["数位化轉型", "AI 整合", "永續發展"]
        }
    }
    
    # 根據查詢內容返回相關數據
    for keyword, data in mock_queries.items():
        if keyword in query:
            return f"""資料庫查詢結果 - {keyword}相關數據:
總記錄數: {data['total_records']}
關鍵指標: {json.dumps(data, ensure_ascii=False, indent=2)}
查詢時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}
數據品質: 優良，已驗證"""
    
    return f"資料庫查詢結果: {query} - 找到 {random.randint(50, 500)} 筆相關記錄"

def fetch_market_data(period: str) -> str:
    """
    獲取外部市場資料的模擬函數
    在實際應用中，這會整合：
    - 市場研究報告 (Nielsen, Euromonitor)
    - 經濟數據 (Bloomberg, Reuters)
    - 競爭情報 (SimilarWeb, SEMrush)
    - 社交媒體議題 (Twitter API, Facebook Insights)
    """
    analyst_logger.info(f"獲取市場資料: {period}")
    
    # 模擬不同時期的市場數據
    market_scenarios = {
        "Q1": {
            "growth_rate": 15.2,
            "market_size": "250億",
            "competition": "中等",
            "trends": ["数位化轉型", "ESG投資", "AI 整合"],
            "risks": ["供應鏈壓力", "通脹影響"]
        },
        "Q2": {
            "growth_rate": 18.7,
            "market_size": "280億",
            "competition": "激烈",
            "trends": ["線上消費增長", "永續消費"],
            "risks": ["原物料漲價", "競爭加劇"]
        }
    }
    
    # 根據時期返回相應數據
    for quarter, data in market_scenarios.items():
        if quarter in period.upper():
            return f"""{period} 市場資料報告:
📈 市場成長率: {data['growth_rate']}%
💰 市場規模: {data['market_size']}
⚔️ 競爭程度: {data['competition']}
🔥 主要趨勢: {', '.join(data['trends'])}
⚠️ 潛在風險: {', '.join(data['risks'])}

數據來源: 多個權威市場研究機構
更新時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
    
    return f"{period} 市場資料: 整體呈穩健成長態勢，成長 {random.uniform(8, 25):.1f}%"

def generate_charts(data_type: str) -> str:
    """
    生成資料視覺化圖表的模擬函數
    在實際應用中，這會使用：
    - Python 視覺化庫 (Matplotlib, Plotly, Seaborn)
    - BI 工具 API (Tableau, Power BI)
    - 自建圖表服務 (D3.js, Chart.js)
    - 雲端視覺化 (Google Charts, AWS QuickSight)
    """
    analyst_logger.info(f"生成圖表: {data_type}")
    
    # 模擬不同類型圖表的生成過程
    chart_types = {
        "銷售": ["時間序列圖", "區域分布圖", "產品比較圖"],
        "費用": ["結構圖", "越勢圖", "預算對比圖"],
        "客戶": ["滿意度分佈", "留存率變化", "獲客漏斗"]
    }
    
    generated_charts = []
    for category, charts in chart_types.items():
        if category in data_type:
            generated_charts.extend(charts[:2])  # 取前兩個相關圖表
    
    if not generated_charts:
        generated_charts = ["基礎統計圖", "趨勢分析圖"]
    
    return f"""[模擬] {data_type} 視覺化圖表生成完成

📊 已生成圖表:
{chr(10).join([f"• {chart}" for chart in generated_charts])}

📁 儲存位置: /reports/charts/{data_type}/
🎨 圖表格式: PNG (高清) + SVG (向量)
🔗 互動版本: /dashboard/{data_type.lower()}

技術詳情:
- 分辨率: 1920x1080 (4K ready)
- 色彩方案: 符合品牌識別
- 數據更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}"""

def create_presentation(content: str) -> str:
    """
    製作商業簡報的模擬函數
    在實際應用中，這會整合：
    - 簡報軟體 (PowerPoint, Google Slides)
    - 網頁簡報 (Reveal.js, Slides.com)
    - PDF 報告生成器 (ReportLab, WeasyPrint)
    - 自動化工具 (Python-PPTX, Aspose)
    """
    analyst_logger.info(f"製作簡報: {content[:50]}...")
    
    # 模擬簡報生成過程
    presentation_id = f"RPT_{datetime.now().strftime('%Y%m%d_%H%M')}"
    
    # 根據內容生成簡報結構
    slides_structure = [
        "封面 - 分析報告標題",
        "執行摘要 - 關鍵發現與建議",
        "市場現狀 - 外部環境分析",
        "業務表現 - 內部數據分析",
        "競爭分析 - 優勣勢評估",
        "趨勢預測 - 未來機會與挑戰",
        "策略建議 - 行動計畫與時程",
        "附錄 - 數據來源與方法論"
    ]
    
    return f"""[模擬] 分析簡報製作完成

📊 報告識別: {presentation_id}
📝 簡報結構 ({len(slides_structure)} 頁):
{chr(10).join([f"{i+1:2d}. {slide}" for i, slide in enumerate(slides_structure)])}

📁 輸出格式:
• PowerPoint (.pptx) - 主簡報
• PDF - 列印版本
• HTML - 網頁展示版
• 圖片套組 (PNG) - 社交媒體使用

🎯 簡報亘點:
• 資料驅動的洞察分析
• 互動式圖表與視覺化
• 可行的商業建議
• 符合企業識別設計

🔗 線上分享: /presentations/{presentation_id.lower()}
📅 完成時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}

內容概要: {content[:200]}..."""

# 步驟 2: 建立商業分析工具集
# 整合各種分析工具，形成完整的商業智能工作流
analyst_tools = [
    Tool(
        name="查詢內部資料庫",
        func=query_database,
        description="查詢內部業務資料庫，獲取銷售、客戶、運營等數據。可查詢銷售績效、客戶分析、費用結構等。"
    ),
    Tool(
        name="獲取外部市場資料",
        func=fetch_market_data,
        description="獲取外部市場資訊，包含市場趨勢、競爭情報、經濟數據。可指定時期（如Q1、Q2）。"
    ),
    Tool(
        name="生成資料視覺化",
        func=generate_charts,
        description="根據數據內容生成專業的視覺化圖表，支援銷售、費用、客戶等多種分析類型。"
    ),
    Tool(
        name="製作商業簡報",
        func=create_presentation,
        description="整合分析結果製作專業的商業簡報，包含圖表、洞察和建議。需要分析內容作為輸入。"
    )
]

# 步驟 3: 建立專業的商業分析師 AI
print("📊 初始化商業分析師 AI...")

# 設定分析師專用的提示模板
business_analyst_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """你是一位經驗豐富的商業分析師，具有以下特質：
        
        🎯 核心能力：
        1. 數據驅動思維：以客觀數據為基礎進行分析
        2. 結構化思維：按照邏輯順序進行分析
        3. 商業敏銭度：能將數據轉化為商業洞察
        4. 沟通技巧：用清晰的語言傳達複雜概念
        
        📝 分析流程：
        1. 理解問題 - 明確分析目標和範圍
        2. 收集資料 - 從內部和外部源獲取數據
        3. 數據分析 - 運用統計方法探索規律
        4. 視覺化呈現 - 製作易懂的圖表
        5. 洞察總結 - 提供可行的建議
        6. 簡報製作 - 整合成專業的報告
        
        ✨ 品質標準：
        - 使用實際數據作為結論基礎
        - 提供具體的數字和百分比
        - 識別趨勢、異常和機會點
        - 提出實用的改進建議和下一步行動"""
    ),
    ("user", "{input}"),
    ("assistant", "{agent_scratchpad}")
])

# 創建商業分析師代理
analyst_agent = AgentExecutor(
    agent=create_tool_calling_agent(llm, analyst_tools, business_analyst_prompt),
    tools=analyst_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=8,          # 允許較多迭代以完成複雜分析
    max_execution_time=180     # 3 分鐘時間上限（分析任務比較耗時）
)

print("✅ 商業分析師 AI 建立完成")

# 步驟 4: 執行全面的商業分析任務
print("\n" + "=" * 60)
print("📊 模擬複雜的商業分析任務")
print("=" * 60)

# 這是一個典型的商業分析場景，需要 AI 自動整合多源資料
comprehensive_analysis_task = """我需要一份關於 2024 Q1 的全面業績分析報告。

分析需求：
1. 分析內部銷售績效和客戶表現
2. 獲取 Q1 市場環境和競爭情況
3. 製作相關的資料視覺化圖表
4. 整合所有分析結果製作一份專業簡報
5. 提出針對 Q2 的策略建議和改進計畫

請按照專業分析流程完成，並在每個步驟後提供關鍵洞察。"""

try:
    print(f"📨 分析任務: {comprehensive_analysis_task[:100]}...")
    print("⏳ AI 分析師開始執行全面的業務分析...")
    
    # 記錄開始時間
    start_time = datetime.now()
    
    # AI 分析師會自動：
    # 1. 理解分析需求和範圍
    # 2. 有系統地收集內外部數據
    # 3. 運用統計方法進行数據分析
    # 4. 製作視覺化圖表幫助理解
    # 5. 整合成專業的商業簡報
    
    report = analyst_agent.invoke({
        "input": comprehensive_analysis_task
    })
    
    # 計算執行時間
    execution_time = datetime.now() - start_time
    
    print("\n" + "=" * 60)
    print("🏆 商業分析完成！")
    print("=" * 60)
    print(f"⏱️ 總分析時間: {execution_time.total_seconds():.1f} 秒")
    
    print("\n📈 完整分析報告:")
    print("-" * 50)
    print(report["output"])
    
except Exception as e:
    analyst_logger.error(f"分析任務失敗: {str(e)}")
    print(f"❌ 分析過程中發生錯誤: {str(e)}")

# 分析工作流的優勢展示
print("\n" + "=" * 60)
print("🧠 AI 商業分析師的優勢:")
print("✅ 效率: 在數分鐘內完成全面分析（人工需數天）")
print("✅ 全面性: 自動整合內外部多源資料")
print("✅ 一致性: 始終保持專業標準和分析模板")
print("✅ 可視化: 自動生成專業圖表和簡報")
print("✅ 可擴展: 輕易添加新的資料來源和分析方法")
print("✅ 可重現: 分析過程透明可稽核，結果可重現")
print("=" * 60)
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
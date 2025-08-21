# LangChain 架構與核心概念

## LangChain 架構概覽

LangChain 框架提供了一系列模組化的抽象化功能（modular abstractions），這些是與 LLM 一起工作所必需的，同時也提供了廣泛的實作版本，方便開發者應用。

```mermaid
graph TB
    subgraph "LangChain v0.2+ 現代架構"
        subgraph "模型層"
            LLM[LLM Models<br/>大型語言模型接入<br/>OpenAI, Anthropic, 本地模型等]
        end
        
        subgraph "輸入處理"
            Prompts[Prompts<br/>提示詞模板管理]
            DocLoad[Document Loaders<br/>文件載入工具]
            Splitters[Text Splitters<br/>文本分割器]
        end
        
        subgraph "核心執行引擎 (LCEL)"
            Runnables[Runnables<br/>可執行接口]
            Chains[Chains/Pipelines<br/>組合式流程]
            LCEL[LCEL 語法<br/>| 管道操作符]
        end
        
        subgraph "進階功能"
            Retrieval[Retrieval<br/>檢索增強生成]
            Memory[Memory<br/>對話記憶]
            OutputParsers[Output Parsers<br/>結構化輸出解析]
            Callbacks[Callbacks<br/>LangSmith 追蹤]
        end
        
        subgraph "智能代理框架"
            Agents[Traditional Agents<br/>工具調用代理]
            LangGraph[LangGraph<br/>多代理工作流<br/>狀態機 & 條件路由]
        end
        
        subgraph "套件生態"
            Core[langchain-core<br/>核心抽象]
            Community[langchain-community<br/>第三方整合]
            Integration[langchain-openai<br/>langchain-chroma<br/>專用整合包]
        end
        
        %% 資料流向
        DocLoad --> Splitters
        Splitters --> Retrieval
        Prompts --> Runnables
        LLM --> Runnables
        Retrieval --> Runnables
        Memory --> Runnables
        
        Runnables --> LCEL
        LCEL --> Chains
        Chains --> OutputParsers
        
        Runnables --> Agents
        Runnables --> LangGraph
        
        %% 監控與追蹤
        Chains -.-> Callbacks
        Agents -.-> Callbacks
        LangGraph -.-> Callbacks
        
        %% 套件依賴
        Core --> Runnables
        Community --> DocLoad
        Integration --> LLM
        Integration --> Retrieval
    end
```

### 主要模組說明

| 模組 | 功能說明 | 實際用途 | v0.2+ 新特性 |
|------|----------|----------|------------|
| **LCEL/Runnables** | 可組合的執行介面 | 用 `\|` 操作符連接各組件，建立資料流管道 | 🆕 核心執行引擎 |
| **LangGraph** | 多代理工作流框架 | 複雜的狀態機、條件路由、多 Agent 協作 | 🆕 取代傳統 Agent |
| **Output Parsers** | 結構化輸出解析 | Pydantic 模型、JSON Schema 驗證 | ✅ 加強類型安全 |
| **LLM Models** | 大型語言模型接入 | 支援 OpenAI GPT、Anthropic Claude、本地模型等 | ✅ 獨立整合包 |
| **Prompts** | 提示詞模板管理 | 支援 ChatPromptTemplate、MessagesPlaceholder | ✅ 強化對話支援 |
| **Document Loaders** | 文件載入工具 | 從 PDF、網頁、資料庫等載入並處理資料 | ✅ 移至 community 包 |
| **Retrieval** | 檢索增強生成 | `create_retrieval_chain` 取代舊 RetrievalQA | ✅ LCEL 原生支援 |
| **Memory** | 對話記憶機制 | `RunnableWithMessageHistory` 新架構 | ✅ 持久化與多會話 |
| **Callbacks** | 執行監控追蹤 | LangSmith 整合、Token 計算、效能分析 | 🆕 可觀測性 |
| **Traditional Agents** | 工具調用代理 | `create_react_agent` 取代 `initialize_agent` | ⚠️ 建議遷移至 LangGraph |

## 什麼是「抽象化」？

### 概念解釋

在軟體設計裡，**抽象化（Abstraction）**就是：
> 隱藏細節，只保留最必要的特徵，讓使用者能更簡單地操作。

- **沒有抽象化** → 你要自己處理一大堆雜事（例如直接呼叫 API，要管 Token、格式、回傳 JSON 等）
- **有抽象化** → 框架幫你把雜事包好，給你一個乾淨的介面

### 實際對比

| 場景 | 沒有抽象化 | 有 LangChain 抽象化 |
|------|------------|-------------------|
| 使用不同 LLM | 要為每個 API 寫不同程式碼 | 統一介面，一行程式碼切換模型 |
| 管理對話記憶 | 手動存取資料庫，拼接上下文 | 掛上 Memory 模組自動處理 |
| 多步驟處理 | 自己設計流程控制邏輯 | 用 Chain 描述步驟即可 |

## LangChain 包裝了哪些複雜功能？

### 1. 🔌 LLM 介接統一化

**原本複雜：** 不同廠牌的 LLM API 格式各異，Token、回傳格式、流式處理都不同。

**LangChain 包裝：** 提供統一的介面，可無痛切換模型。

```python
# 匯入不同廠商的聊天模型類別
from langchain_openai import ChatOpenAI      # OpenAI GPT 系列模型
from langchain_anthropic import ChatAnthropic # Anthropic Claude 系列模型

# 統一的模型初始化介面 - 這是 LangChain 抽象化的核心價值
# 無論使用哪家廠商的模型，初始化語法都保持一致
llm = ChatOpenAI(model="gpt-4")  
# 或者切換到 Claude 模型，只需要改這一行
# llm = ChatAnthropic(model="claude-3-opus")

# 統一的調用介面 - invoke() 方法對所有模型都相同
# 不需要學習每家廠商的專屬 API 格式
response = llm.invoke("幫我寫一首詩")
print(response.content)  # 所有模型的回應都有統一的 .content 屬性
```

### 2. 📝 Prompt 模板管理

**原本複雜：** 要自己拼字串，把上下文、格式、變數全都寫死。

**LangChain 包裝：** 提供 PromptTemplate，可以用變數填入。

```python
# 匯入提示範本類別
from langchain.prompts import PromptTemplate

# 建立提示範本 - 使用 {} 語法定義可替換的變數
# 這樣可以重複使用同一個範本，只需要傳入不同的資料
template = PromptTemplate.from_template(
    "你是一位營養師，請根據這些數據 {health_data} 提供建議"
)

# 將實際資料填入範本變數
# format() 方法會將 {health_data} 替換為實際的健康數據
prompt = template.format(health_data="血糖偏高")
print(prompt)
# 輸出: "你是一位營養師，請根據這些數據 血糖偏高 提供建議"

# 範本的優勢：可以重複使用，只需要改變輸入資料
another_prompt = template.format(health_data="膽固醇過高，BMI 28.5")
```

### 3. 🧠 Memory（對話記憶）

**原本複雜：** LLM 天生無記憶，要自己管理對話歷史，存資料庫，再手動拼接。

**LangChain 包裝：** 內建各種 Memory 類型，掛上就能記住上下文。

```python
# v0.2+ 新版對話記憶做法 - 使用 RunnableWithMessageHistory 管理對話狀態
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# 初始化 LLM 模型
llm = ChatOpenAI(model="gpt-4o-mini")

# MessagesPlaceholder 的底層資料結構是訊息列表
# 每個訊息都是字典格式，包含 role 和 content
"""
對話歷史的資料結構範例：
[
  {"role": "user", "content": "我叫小明"},
  {"role": "assistant", "content": "好的，小明，我記住了。"}
]
"""

# 建立聊天提示範本 - 包含系統訊息、歷史記錄和使用者輸入
prompt = ChatPromptTemplate.from_messages([
    # 系統訊息：定義 AI 助手的角色和行為
    ("system", "你是一個有用的助手，能記住對話歷史。"),
    
    # 對話歷史佔位符：動態插入之前的對話記錄
    MessagesPlaceholder(variable_name="chat_history"),
    
    # 當前使用者輸入
    ("human", "{input}"),
])

# 使用 LCEL 管道語法組合提示範本和 LLM
chain = prompt | llm

# 建立記憶體存儲 - 使用字典在記憶體中保存不同會話的歷史
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    """根據會話 ID 獲取或建立對話歷史
    
    Args:
        session_id: 唯一的會話識別碼，用於區分不同使用者或對話
    
    Returns:
        ChatMessageHistory: 該會話的對話歷史物件
    """
    if session_id not in store:
        # 如果是新會話，建立空的對話歷史
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 建立具有記憶功能的對話鏈
conversation = RunnableWithMessageHistory(
    chain,                           # 要執行的鏈（提示範本 + LLM）
    get_session_history,            # 獲取會話歷史的函數
    input_messages_key="input",     # 使用者輸入的鍵名
    history_messages_key="chat_history",  # 對話歷史的鍵名
)

# 設定會話配置 - 指定會話 ID
config = {"configurable": {"session_id": "user123"}}

# 第一次對話：建立記憶
first_response = conversation.invoke({"input": "我叫小明"}, config=config)
print(f"第一次回應: {first_response.content}")

# 第二次對話：測試記憶功能
result = conversation.invoke({"input": "我剛才說我叫什麼名字？"}, config=config)
print(f"記憶測試結果: {result.content}")
# AI 應該能夠記住之前提到的「小明」這個名字

# 檢視當前會話的對話歷史
history = store["user123"]
print(f"\n對話歷史共有 {len(history.messages)} 條訊息")
for i, msg in enumerate(history.messages):
    print(f"{i+1}. {msg.type}: {msg.content}")
```

### 4. 🔍 Retrieval + 外部知識庫整合

**原本複雜：** 要自己寫 embedding、存到向量資料庫、再寫檢索邏輯。

**LangChain 包裝：** 提供 Retriever，一句話就能讓 LLM 接外部知識。

```python
# 檢索增強生成 (RAG) 的 v0.2+ 新版實作
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 建立文件處理的提示範本
# {context} 會被自動填入檢索到的相關文件內容
# {input} 是使用者的問題
prompt = ChatPromptTemplate.from_template(
    "根據以下文件回覆：{context}\n\n問題：{input}\n\n請基於提供的文件內容回答，如果文件中沒有相關資訊，請明確說明。"
)

# 建立文件合併鏈 - 將多個檢索到的文件合併後送給 LLM
# "stuff" 策略：將所有相關文件直接塞入 prompt 中
stuff_chain = create_stuff_documents_chain(
    llm,     # 語言模型
    prompt   # 包含 context 和 input 的提示範本
)

# 建立完整的檢索-回答鏈
# 這個鏈會：1) 根據問題檢索相關文件 → 2) 將文件和問題送給 LLM 生成回答
qa = create_retrieval_chain(
    vectorstore.as_retriever(),  # 向量資料庫檢索器（需事先建立）
    stuff_chain                  # 文件處理和回答生成鏈
)

# 執行問答
answer = qa.invoke({"input": "公司的請假政策是什麼？"})

# 檢視結果
print(f"回答: {answer['answer']}")

# 可選：檢視檢索到的相關文件
if 'context' in answer:
    print(f"\n參考文件數量: {len(answer['context'])}")
    for i, doc in enumerate(answer['context']):
        print(f"文件 {i+1}: {doc.page_content[:100]}...")
```

### 5. ⛓️ Chains（多步驟流程組裝）

**原本複雜：** 要手動控制流程：先檢索資料 → 再問 LLM → 再格式化結果。

**LangChain 包裝：** 把多步驟組裝成「流程鏈」。

```python
# v0.2+ 新版序列鏈做法：使用 LCEL (LangChain Expression Language) 管道語法
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 初始化 LLM 模型
llm = ChatOpenAI(model="gpt-4o-mini")

# 步驟 1：健康數據分析的提示範本
prompt_analysis = PromptTemplate.from_template(
    "作為專業醫療顧問，請詳細分析以下健康數據：{health_data}\n"
    "請從以下角度分析：1) 各項指標的正常範圍比較 2) 潛在健康風險 3) 相互關聯性"
)

# 步驟 2：基於分析結果提供建議的提示範本
prompt_recommendation = PromptTemplate.from_template(
    "基於以下健康分析結果：{analysis}\n\n"
    "請提供具體的改善建議，包括：1) 飲食調整 2) 運動計劃 3) 生活習慣改變 4) 是否需要就醫"
)

# 步驟 3：將建議格式化為友好報告的提示範本
prompt_format = PromptTemplate.from_template(
    "請將以下健康建議：{recommendations}\n\n"
    "格式化為結構清晰、易讀的個人健康報告，使用友好的語調和明確的行動步驟"
)

# 使用 LCEL 管道語法（| 操作符）建立各個處理鏈
# 每個鏈都包含：提示範本 → LLM → 輸出解析器
analysis_chain = prompt_analysis | llm | StrOutputParser()
recommendation_chain = prompt_recommendation | llm | StrOutputParser()
format_chain = prompt_format | llm | StrOutputParser()

# 完整的健康分析流程函數
def health_analysis_pipeline(health_data: str):
    """多步驟健康分析流程
    
    Args:
        health_data: 原始健康數據字串
        
    Returns:
        str: 格式化的健康分析報告
    """
    print("步驟 1: 分析健康數據...")
    # 第一步：分析原始健康數據
    analysis = analysis_chain.invoke({"health_data": health_data})
    print(f"分析結果: {analysis[:100]}...\n")
    
    print("步驟 2: 生成改善建議...")
    # 第二步：基於分析結果生成建議
    recommendations = recommendation_chain.invoke({"analysis": analysis})
    print(f"建議內容: {recommendations[:100]}...\n")
    
    print("步驟 3: 格式化最終報告...")
    # 第三步：將建議格式化為用戶友好的報告
    final_report = format_chain.invoke({"recommendations": recommendations})
    
    return final_report

# 使用範例
health_data = "血糖偏高 130mg/dL, BMI 25.5, 運動量少, 血壓 140/90, 睡眠品質差"
result = health_analysis_pipeline(health_data)
print("=== 最終健康分析報告 ===")
print(result)

# LCEL 管道語法的優勢：
# 1. 程式碼簡潔：用 | 操作符直觀表達資料流
# 2. 型別安全：編譯時檢查介面相容性
# 3. 可組合性：可以輕鬆重新排列或替換組件
# 4. 並行支援：某些操作可以自動並行化
```

### 6. 🎯 Agents（動態決策 & 工具調用）

**原本複雜：** 要自己寫 if/else 判斷，決定何時該查 API、何時直接回覆。

**LangChain 包裝：** LLM 自主決定該調用哪個工具。

```python
# Agent 系統：讓 LLM 能夠自主決策和使用工具
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
import re
import operator

# 安全數學計算器實作 - 避免使用危險的 eval() 函數
def safe_calculate(expression: str) -> str:
    """安全的數學計算器，只允許基本數學運算
    
    Args:
        expression: 數學表達式字串（如 "(100+50)*2"）
        
    Returns:
        str: 計算結果或錯誤訊息
    """
    try:
        # 移除所有空白字符
        expression = expression.replace(" ", "")
        
        # 安全檢查：只允許數字、基本運算符和括號
        allowed_chars = set("0123456789+-*/().")
        if not all(c in allowed_chars for c in expression):
            return "錯誤：包含不允許的字符，只支援 +, -, *, /, (, ) 和數字"
        
        # 使用 eval() 的安全替代方案（簡化版本）
        # 在生產環境中，建議使用更安全的數學解析器
        result = eval(expression, {"__builtins__": {}}, {})
        return f"計算結果: {expression} = {result}"
        
    except ZeroDivisionError:
        return "錯誤：除零錯誤"
    except SyntaxError:
        return "錯誤：數學表達式語法錯誤"
    except Exception as e:
        return f"錯誤：計算失敗 - {str(e)}"

# 建立工具集 - Agent 可以使用的功能清單
tools = [
    Tool(
        name="安全計算器",
        func=safe_calculate,
        description="安全的數學計算器，支援基本四則運算和括號。輸入格式：數學表達式字串。例如：'(100+50)*2'"
    )
]

# 初始化 LLM - 設定 temperature=0 確保回應的一致性
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 建立 Agent 的提示範本
prompt = ChatPromptTemplate.from_messages([
    # 系統指令：定義 Agent 的角色和行為
    ("system", "你是一個智能助手，能夠使用提供的工具來完成任務。"
               "當使用者提出需要計算的問題時，請使用安全計算器工具。"
               "請先分析問題，然後選擇合適的工具，最後提供清晰的回答。"),
    
    # 使用者輸入
    ("user", "{input}"),
    
    # Agent 的思考過程記錄（scratchpad）
    # 這裡會記錄 Agent 的決策過程和工具調用結果
    ("assistant", "{agent_scratchpad}"),
])

# 建立 Tool-Calling Agent
# 這種 Agent 能夠：1) 理解使用者意圖 2) 選擇合適工具 3) 調用工具 4) 解釋結果
agent = create_tool_calling_agent(
    llm,      # 語言模型
    tools,    # 可用工具列表
    prompt    # Agent 的提示範本
)

# 建立 Agent 執行器 - 負責管理 Agent 的執行流程
agent_executor = AgentExecutor(
    agent=agent,           # Agent 實例
    tools=tools,          # 工具列表（與 agent 中的相同）
    verbose=True,         # 啟用詳細輸出，可以看到 Agent 的思考過程
    max_iterations=5,     # 最大迭代次數，防止無限循環
    return_intermediate_steps=True  # 返回中間步驟，便於調試
)

# 測試複雜數學計算任務
print("=== Agent 執行數學計算任務 ===")
response = agent_executor.invoke({
    "input": "幫我計算 (100+50)*2 的結果，然後再除以 3"
})

print(f"\n最終回答: {response['output']}")

# 檢視 Agent 的執行步驟
if 'intermediate_steps' in response:
    print("\n=== Agent 執行步驟 ===")
    for i, (action, observation) in enumerate(response['intermediate_steps']):
        print(f"步驟 {i+1}:")
        print(f"  動作: {action.tool} - {action.tool_input}")
        print(f"  結果: {observation}")

# Agent 系統的優勢：
# 1. 自主決策：LLM 能根據問題自動選擇使用哪個工具
# 2. 多步驟推理：可以將複雜任務分解為多個步驟
# 3. 錯誤處理：當工具調用失敗時，Agent 可以嘗試其他方法
# 4. 可解釋性：能夠解釋為什麼選擇特定工具和如何得出結果
```

## 核心架構理念

### 模組化設計

LangChain 採用模組化設計，每個組件都可以獨立使用或組合使用：

- **可組合性**：不同模組可以靈活組合
- **可擴展性**：容易添加新的模型和工具
- **可替換性**：同類型的組件可以互相替換

### 統一的介面抽象

所有 LangChain 組件都實現統一的 `Runnable` 介面：

- **invoke()**：同步執行
- **ainvoke()**：異步執行  
- **batch()**：批量處理
- **stream()**：流式處理

### 聲明式程式設計

v0.2+ 的 LCEL 語法讓開發者可以用聲明式的方式描述資料流：

```python
# LCEL 聲明式 vs 命令式程式設計比較

# === 聲明式寫法 (LCEL) ===
# 使用管道操作符 | 描述資料流，簡潔直觀
chain = prompt | llm | output_parser

# 執行聲明式鏈
result = chain.invoke({"question": "什麼是人工智慧？"})

# === 等效的命令式寫法 ===
def imperative_chain(input_data):
    """命令式實作：手動控制每個步驟的執行順序
    
    Args:
        input_data: 輸入資料字典
        
    Returns:
        解析後的最終結果
    """
    # 步驟 1：格式化提示範本
    print("步驟 1: 格式化提示範本...")
    prompt_result = prompt.format(**input_data)
    print(f"提示內容: {prompt_result[:50]}...")
    
    # 步驟 2：調用 LLM 生成回應
    print("步驟 2: 調用 LLM 生成回應...")
    llm_result = llm.invoke(prompt_result)
    print(f"LLM 回應: {llm_result.content[:50]}...")
    
    # 步驟 3：解析輸出格式
    print("步驟 3: 解析輸出格式...")
    final_result = output_parser.parse(llm_result)
    print(f"最終結果: {final_result}")
    
    return final_result

# 執行命令式版本
result = imperative_chain({"question": "什麼是人工智慧？"})

# === 兩種寫法的比較 ===
"""
聲明式 (LCEL) 的優勢：
1. 程式碼簡潔：一行描述整個資料流
2. 可讀性高：| 操作符直觀表達「然後」的概念
3. 自動最佳化：框架可以自動並行化某些操作
4. 型別檢查：編譯時檢查各組件間的介面相容性
5. 內建功能：自動支援 streaming、async、batch 等功能

命令式的特點：
1. 控制精細：可以在每步之間插入自定義邏輯
2. 除錯容易：可以單步除錯每個步驟
3. 傳統思維：更符合傳統程式設計習慣
4. 靈活度高：可以加入條件判斷和迴圈控制
"""

# === LCEL 進階功能展示 ===
from langchain_core.runnables import RunnableParallel

# 並行處理：同時執行多個不同的分析
parallel_chain = RunnableParallel({
    "summary": prompt_summary | llm | output_parser,    # 摘要分析
    "sentiment": prompt_sentiment | llm | output_parser, # 情感分析
    "keywords": prompt_keywords | llm | output_parser   # 關鍵字提取
})

# 一次執行多個分析任務，自動並行化提升效率
parallel_result = parallel_chain.invoke({"text": "這是一段要分析的文本..."}) 
print(f"摘要: {parallel_result['summary']}")
print(f"情感: {parallel_result['sentiment']}")
print(f"關鍵字: {parallel_result['keywords']}")
```

## 總結

LangChain 包裝的就是「LLM 開發的重複繁瑣工作」：

- ✅ **統一的模型介面** - 一套程式碼支援多種 LLM
- ✅ **智慧記憶管理** - 自動處理對話上下文
- ✅ **檢索增強生成** - 簡化外部知識整合
- ✅ **結構化輸出** - 可靠的資料格式轉換
- ✅ **工具調用框架** - 讓 LLM 能夠執行動作
- ✅ **可觀測性支援** - 內建監控和除錯功能
- ✅ **模組化設計** - 靈活組合各種功能

讓你專注在**應用邏輯和 Prompt 設計**，而不是一直「重造輪子」。

---

::: tip 深入學習
現在你已經了解 LangChain 的架構與核心概念，接下來可以深入學習各個專門主題：

- [LCEL 表達式語言](/tutorials/lcel) - 學習管道語法和組合模式
- [LangGraph 工作流](/tutorials/langgraph) - 掌握多代理協作框架  
- [結構化輸出解析](/tutorials/output-parsers) - 實現可靠的資料轉換
- [記憶機制與對話管理](/tutorials/memory-systems) - 建構智慧對話系統
- [監控與可觀測性](/tutorials/monitoring) - 生產環境最佳實踐
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
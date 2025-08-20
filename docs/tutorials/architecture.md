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
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# 換模型只換這行，其他程式不用改
llm = ChatOpenAI(model="gpt-4")  
# 或 llm = ChatAnthropic(model="claude-3-opus")

response = llm.invoke("幫我寫一首詩")
```

### 2. 📝 Prompt 模板管理

**原本複雜：** 要自己拼字串，把上下文、格式、變數全都寫死。

**LangChain 包裝：** 提供 PromptTemplate，可以用變數填入。

```python
from langchain.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "你是一位營養師，請根據這些數據 {health_data} 提供建議"
)

prompt = template.format(health_data="血糖偏高")
```

### 3. 🧠 Memory（對話記憶）

**原本複雜：** LLM 天生無記憶，要自己管理對話歷史，存資料庫，再手動拼接。

**LangChain 包裝：** 內建各種 Memory 類型，掛上就能記住上下文。

```python
# v0.2+ 新版對話記憶做法（修正 placeholder 用法）
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

# MessagesPlaceholder 底層實作估計為字典，
"""
[
  {"role": "user", "content": "我叫小明"},
  {"role": "assistant", "content": "好的，小明，我記住了。"}
]
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一個有用的助手，能記住對話歷史。"),
    MessagesPlaceholder(variable_name="chat_history"),   # ← 正確寫法
    ("human", "{input}"),
])

chain = prompt | llm

# 簡易 In-Memory 記憶存放
store = {}
def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

config = {"configurable": {"session_id": "user123"}}
conversation.invoke({"input": "我叫小明"}, config=config)
result = conversation.invoke({"input": "我剛才說我叫什麼名字？"}, config=config)
print(result.content)

```

### 4. 🔍 Retrieval + 外部知識庫整合

**原本複雜：** 要自己寫 embedding、存到向量資料庫、再寫檢索邏輯。

**LangChain 包裝：** 提供 Retriever，一句話就能讓 LLM 接外部知識。

```python
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 自動檢索相關文件並回答（v0.2+ 新版做法）
prompt = ChatPromptTemplate.from_template("根據以下文件回覆：{context}\n問題：{input}")
stuff_chain = create_stuff_documents_chain(llm, prompt)
qa = create_retrieval_chain(vectorstore.as_retriever(), stuff_chain)

answer = qa.invoke({"input": "公司的請假政策是什麼？"})
print(answer["answer"])
```

### 5. ⛓️ Chains（多步驟流程組裝）

**原本複雜：** 要手動控制流程：先檢索資料 → 再問 LLM → 再格式化結果。

**LangChain 包裝：** 把多步驟組裝成「流程鏈」。

```python
# v0.2+ 新版序列鏈做法：使用 LCEL 管道語法
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

# 定義各步驟
prompt_analysis = PromptTemplate.from_template("分析以下健康数據：{health_data}")
prompt_recommendation = PromptTemplate.from_template("基於分析結果 {analysis} 提供具體建議")
prompt_format = PromptTemplate.from_template("將以下建議 {recommendations} 格式化為用戶友好的報告")

# 使用 LCEL 管道語法串接（| 操作符）
analysis_chain = prompt_analysis | llm | StrOutputParser()
recommendation_chain = prompt_recommendation | llm | StrOutputParser()
format_chain = prompt_format | llm | StrOutputParser()

# 完整的健康分析流程
def health_analysis_pipeline(health_data: str):
    analysis = analysis_chain.invoke({"health_data": health_data})
    recommendations = recommendation_chain.invoke({"analysis": analysis})
    final_report = format_chain.invoke({"recommendations": recommendations})
    return final_report

# 使用範例
result = health_analysis_pipeline("血糖偏高 130mg/dL, BMI 25.5, 運動量少")
print(result)
```

### 6. 🎯 Agents（動態決策 & 工具調用）

**原本複雜：** 要自己寫 if/else 判斷，決定何時該查 API、何時直接回覆。

**LangChain 包裝：** LLM 自主決定該調用哪個工具。

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate

# 安全計算器（詳細實現請參考介紹章節）
def safe_calculate(expression: str):
    """安全的數學計算器，避免使用 eval()"""
    # 實現安全的數學計算邏輯
    return f"計算結果: {expression}"

# 安全的工具集
tools = [
    Tool(name="安全計算", func=safe_calculate, description="安全的數學計算（只允許 +, -, *, /, ** 運算）")
]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一個有用的助手。使用提供的工具來完成任務。"),
    ("user", "{input}"),
    ("assistant", "{agent_scratchpad}"),
])

# LLM 能自主決定使用哪個工具
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 複雜任務自主分解與執行
response = agent_executor.invoke({
    "input": "幫我計算 (100+50)*2 的結果"
})
print(response["output"])
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
# 聲明式的資料流描述
chain = prompt | llm | output_parser

# 等效於命令式的寫法
def imperative_chain(input_data):
    prompt_result = prompt.format(**input_data)
    llm_result = llm.invoke(prompt_result)
    final_result = output_parser.parse(llm_result)
    return final_result
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
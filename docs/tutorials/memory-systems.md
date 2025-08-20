# 記憶機制與對話管理

## LangChain v0.2+ 記憶架構變革

傳統的記憶機制已被更強大且靈活的 `RunnableWithMessageHistory` 取代，提供更好的持久化和多會話支持。

### 核心架構變化

```mermaid
graph TB
    subgraph "v0.2+ 新版記憶架構"
        A[Message History Store] --> B[RunnableWithMessageHistory]
        B --> C[Session Management]
        C --> D[Persistent Storage]
        
        subgraph "支援的儲存後端"
            D --> E[ChatMessageHistory]
            D --> F[RedisChatMessageHistory]
            D --> G[PostgresChatMessageHistory]
            D --> H[Custom Storage]
        end
        
        subgraph "記憶類型"
            I[ConversationBufferMemory]
            J[ConversationSummaryMemory]
            K[ConversationBufferWindowMemory]
            L[VectorStoreRetrieverMemory]
        end
        
        B --> I
        B --> J
        B --> K
        B --> L
    end
```

## 新版記憶實現

### 1. 基本對話記憶

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# 建立對話模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一個有用的助手，能記住對話歷史。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

# 建立基本對話鏈
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
chain = prompt | llm

# 記憶儲存
store = {}
def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 帶記憶的對話鏈
conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# 多輪對話
config = {"configurable": {"session_id": "user_123"}}

# 第一輪
response1 = conversation.invoke(
    {"input": "我叫小明，今年 25 歲"},
    config=config
)
print(response1.content)

# 第二輪 - AI 會記住前面的資訊
response2 = conversation.invoke(
    {"input": "我剛才說我幾歲？"},
    config=config
)
print(response2.content)  # 會回答「你說你今年 25 歲」
```

### 2. 持久化記憶儲存

```python
# Redis 持久化記憶
from langchain_community.chat_message_histories import RedisChatMessageHistory

def get_redis_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(
        session_id=session_id,
        url="redis://localhost:6379/0",
        key_prefix="chat_history:",
        ttl=86400  # 24 小時過期
    )

# PostgreSQL 持久化記憶
from langchain_community.chat_message_histories import PostgresChatMessageHistory

def get_postgres_history(session_id: str) -> PostgresChatMessageHistory:
    return PostgresChatMessageHistory(
        connection_string="postgresql://user:pass@localhost/chatdb",
        session_id=session_id,
        table_name="chat_histories"
    )

# 使用持久化儲存
persistent_conversation = RunnableWithMessageHistory(
    chain,
    get_redis_history,  # 或 get_postgres_history
    input_messages_key="input",
    history_messages_key="chat_history",
)
```

### 3. 智能記憶管理

```python
from langchain.memory import ConversationSummaryBufferMemory

class IntelligentMemoryManager:
    def __init__(self, max_token_limit=4000):
        self.max_token_limit = max_token_limit
        self.memory = ConversationSummaryBufferMemory(
            llm=ChatOpenAI(model="gpt-4o-mini"),
            max_token_limit=max_token_limit,
            return_messages=True
        )
    
    def get_relevant_history(self, current_input: str, session_id: str):
        """獲取與當前輸入最相關的歷史記錄"""
        # 使用向量搜索找到相關對話
        history = self.memory.chat_memory.messages
        
        # 簡化的相關性計算（實際應用中可使用 embedding）
        relevant_messages = []
        for message in history[-10:]:  # 取最近 10 條
            if any(word in message.content.lower() 
                  for word in current_input.lower().split()):
                relevant_messages.append(message)
        
        return relevant_messages

# 智能記憶對話系統
class SmartConversationSystem:
    def __init__(self):
        self.memory_manager = IntelligentMemoryManager()
        self.llm = ChatOpenAI(model="gpt-4o-mini")
    
    def chat(self, user_input: str, session_id: str):
        # 獲取相關歷史
        relevant_history = self.memory_manager.get_relevant_history(
            user_input, session_id
        )
        
        # 構建動態 prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "基於以下相關對話歷史回答問題"),
            *[(msg.type, msg.content) for msg in relevant_history],
            ("human", user_input)
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"input": user_input})
        
        # 更新記憶
        self.memory_manager.memory.save_context(
            {"input": user_input},
            {"output": response.content}
        )
        
        return response.content
```

### 4. 多類型記憶整合

```python
class MultiModalMemorySystem:
    """多模式記憶系統"""
    
    def __init__(self):
        # 短期記憶：最近的對話
        self.short_term = ChatMessageHistory()
        
        # 長期記憶：重要資訊摘要
        self.long_term = ConversationSummaryMemory(
            llm=ChatOpenAI(model="gpt-4o-mini")
        )
        
        # 向量記憶：語義搜索
        from langchain.memory import VectorStoreRetrieverMemory
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings
        
        vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
        self.vector_memory = VectorStoreRetrieverMemory(
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
        )
    
    def process_conversation(self, user_input: str, ai_response: str):
        """處理對話並更新所有記憶類型"""
        
        # 更新短期記憶
        self.short_term.add_user_message(user_input)
        self.short_term.add_ai_message(ai_response)
        
        # 更新長期記憶（定期總結）
        if len(self.short_term.messages) % 10 == 0:
            summary = self.long_term.predict_new_summary(
                self.short_term.messages[-10:],
                self.long_term.moving_summary_buffer
            )
            self.long_term.moving_summary_buffer = summary
        
        # 更新向量記憶（重要對話）
        if self._is_important_conversation(user_input, ai_response):
            self.vector_memory.save_context(
                {"input": user_input},
                {"output": ai_response}
            )
    
    def _is_important_conversation(self, user_input: str, ai_response: str) -> bool:
        """判斷是否為重要對話"""
        important_keywords = ["重要", "記住", "記錄", "關鍵", "問題"]
        return any(keyword in user_input for keyword in important_keywords)
    
    def retrieve_context(self, query: str) -> str:
        """檢索相關上下文"""
        contexts = []
        
        # 短期記憶
        recent_context = "\n".join([
            f"{msg.type}: {msg.content}" 
            for msg in self.short_term.messages[-6:]
        ])
        contexts.append(f"最近對話：\n{recent_context}")
        
        # 長期記憶
        if self.long_term.moving_summary_buffer:
            contexts.append(f"對話摘要：\n{self.long_term.moving_summary_buffer}")
        
        # 向量記憶
        relevant_docs = self.vector_memory.retriever.get_relevant_documents(query)
        if relevant_docs:
            vector_context = "\n".join([doc.page_content for doc in relevant_docs])
            contexts.append(f"相關歷史：\n{vector_context}")
        
        return "\n\n".join(contexts)
```

## 記憶機制最佳實踐

### 1. 記憶類型選擇指南

| 使用場景 | 推薦記憶類型 | 原因 |
|----------|------------|------|
| **短期客服對話** | ConversationBufferWindowMemory | 只需記住最近幾輪對話 |
| **長期個人助手** | ConversationSummaryBufferMemory | 平衡詳細度與長度 |
| **知識問答系統** | VectorStoreRetrieverMemory | 語義搜索歷史相關問題 |
| **多用戶系統** | RunnableWithMessageHistory + Redis | 可擴展性與持久化 |
| **企業級應用** | 多模式記憶整合 | 全面的上下文管理 |

### 2. 性能優化策略

```python
# 記憶壓縮與清理
class OptimizedMemoryManager:
    def __init__(self, max_messages=100):
        self.max_messages = max_messages
        self.compression_threshold = 50
    
    def compress_memory_if_needed(self, memory):
        """智能記憶壓縮"""
        if len(memory.messages) > self.compression_threshold:
            # 保留最近的重要對話
            important_messages = self._extract_important_messages(
                memory.messages
            )
            # 總結舊對話
            summary = self._summarize_old_messages(
                memory.messages[:-20]
            )
            # 重構記憶
            memory.clear()
            memory.add_message(summary)
            memory.messages.extend(important_messages)
    
    def _extract_important_messages(self, messages):
        """提取重要訊息"""
        # 實現重要性評分邏輯
        pass
    
    def _summarize_old_messages(self, old_messages):
        """總結舊訊息"""
        # 實現總結邏輯
        pass
```

### 3. 多會話管理

```python
class SessionManager:
    def __init__(self):
        self.active_sessions = {}
        self.session_timeout = 3600  # 1小時
    
    def get_or_create_session(self, user_id: str, session_type: str = "default"):
        """獲取或創建會話"""
        session_key = f"{user_id}_{session_type}"
        
        if session_key not in self.active_sessions:
            self.active_sessions[session_key] = {
                "memory": ChatMessageHistory(),
                "created_at": time.time(),
                "last_activity": time.time()
            }
        
        # 更新活動時間
        self.active_sessions[session_key]["last_activity"] = time.time()
        return self.active_sessions[session_key]["memory"]
    
    def cleanup_expired_sessions(self):
        """清理過期會話"""
        current_time = time.time()
        expired_sessions = [
            key for key, session in self.active_sessions.items()
            if current_time - session["last_activity"] > self.session_timeout
        ]
        
        for key in expired_sessions:
            del self.active_sessions[key]
```

## 實際應用範例

### 智能客服記憶系統

```python
class CustomerServiceMemory:
    def __init__(self):
        self.customer_profiles = {}  # 客戶檔案
        self.conversation_history = {}  # 對話歷史
        self.issue_tracking = {}  # 問題追蹤
    
    def get_customer_context(self, customer_id: str, current_query: str):
        """獲取客戶上下文"""
        # 客戶檔案
        profile = self.customer_profiles.get(customer_id, {})
        
        # 歷史對話
        history = self.conversation_history.get(customer_id, [])
        
        # 相關問題
        similar_issues = self._find_similar_issues(current_query)
        
        context = {
            "customer_profile": profile,
            "conversation_history": history[-5:],  # 最近5次對話
            "similar_issues": similar_issues,
            "current_query": current_query
        }
        
        return context
    
    def update_customer_context(self, customer_id: str, 
                              interaction_data: dict):
        """更新客戶上下文"""
        # 更新客戶檔案
        if customer_id not in self.customer_profiles:
            self.customer_profiles[customer_id] = {}
        
        # 提取客戶資訊
        self._extract_customer_info(customer_id, interaction_data)
        
        # 更新對話歷史
        if customer_id not in self.conversation_history:
            self.conversation_history[customer_id] = []
        
        self.conversation_history[customer_id].append({
            "timestamp": datetime.now(),
            "query": interaction_data.get("query"),
            "response": interaction_data.get("response"),
            "satisfaction": interaction_data.get("satisfaction")
        })
```

### 教育對話系統

```python
class EducationalChatMemory:
    """教育對話系統記憶"""
    
    def __init__(self):
        self.student_progress = {}
        self.learning_patterns = {}
        self.difficulty_adjustments = {}
    
    def track_learning_progress(self, student_id: str, 
                              topic: str, performance: dict):
        """追蹤學習進度"""
        if student_id not in self.student_progress:
            self.student_progress[student_id] = {}
        
        if topic not in self.student_progress[student_id]:
            self.student_progress[student_id][topic] = {
                "attempts": 0,
                "correct_answers": 0,
                "difficulty_level": 1,
                "last_session": None
            }
        
        progress = self.student_progress[student_id][topic]
        progress["attempts"] += 1
        
        if performance.get("correct"):
            progress["correct_answers"] += 1
        
        progress["last_session"] = datetime.now()
        
        # 調整難度
        self._adjust_difficulty(student_id, topic)
    
    def get_personalized_context(self, student_id: str, topic: str):
        """獲取個人化上下文"""
        progress = self.student_progress.get(student_id, {}).get(topic, {})
        
        context = {
            "current_level": progress.get("difficulty_level", 1),
            "success_rate": self._calculate_success_rate(progress),
            "weak_areas": self._identify_weak_areas(student_id),
            "learning_style": self._detect_learning_style(student_id)
        }
        
        return context
```

## 總結

LangChain v0.2+ 的記憶機制提供了：

- 🔄 **統一的記憶介面** - RunnableWithMessageHistory 統一管理
- 💾 **多種持久化選項** - Redis、PostgreSQL、自定義儲存
- 🧠 **智能記憶管理** - 自動壓縮、相關性搜索
- 👥 **多會話支持** - 並行處理多個用戶會話
- 🎯 **上下文感知** - 基於歷史的智能回應
- ⚡ **性能優化** - 記憶壓縮和過期清理

選擇合適的記憶策略，結合良好的會話管理，能夠建構出真正智能的對話系統。

---

::: tip 下一步
現在你已經掌握了記憶機制，接下來可以：
1. [監控與可觀測性](/tutorials/monitoring) - 監控記憶系統的性能
2. [進階應用案例](/tutorials/advanced-examples) - 查看企業級記憶系統實現
3. 結合 [LangGraph](/tutorials/langgraph) 建構有狀態的智能工作流
:::

::: warning 實踐建議
- **合理選擇記憶類型**：根據應用場景選擇最適合的記憶策略
- **定期清理記憶**：避免記憶過度膨脹影響性能
- **保護隱私資料**：敏感資訊應加密存儲或定期清除
- **監控記憶使用**：追蹤記憶大小和檢索效率
:::
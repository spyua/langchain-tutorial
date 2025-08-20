# 結構化輸出解析器 (Output Parsers)

## 為什麼需要結構化輸出？

LLM 的原始輸出通常是非結構化的文字，但實際應用中我們經常需要結構化資料來進行後續處理。

### 問題場景
```python
# ❌ 原始 LLM 輸出：難以程式化處理
response = llm.invoke("分析這篇文章的情感")
print(response.content)  # "這篇文章整體情感偏向正面，信心指數約 85%，主要情感類別是樂觀..."

# 😤 需要手動解析字串，容易出錯
if "正面" in response.content:
    sentiment = "positive"
else:
    sentiment = "negative"
```

### 解決方案：結構化輸出
```python
# ✅ 使用 Output Parser：獲得結構化資料
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class SentimentAnalysis(BaseModel):
    sentiment: str = Field(description="情感傾向：positive, negative, neutral")
    confidence: float = Field(description="信心指數 0-1", ge=0, le=1)
    emotions: list[str] = Field(description="檢測到的情感清單")
    summary: str = Field(description="分析總結")

parser = PydanticOutputParser(pydantic_object=SentimentAnalysis)
chain = prompt | llm | parser

result = chain.invoke({"text": "今天天氣真好！"})
print(result)  # SentimentAnalysis 物件
print(result.sentiment)     # "positive"
print(result.confidence)    # 0.95
print(result.emotions)      # ["happiness", "optimism"]
```

## Output Parser 類型總覽

### 1. Pydantic Output Parser
**最推薦的結構化輸出方式**

```python
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class TaskExtraction(BaseModel):
    """任務提取結果"""
    tasks: List[str] = Field(description="提取的任務清單")
    priority: str = Field(description="優先級：high, medium, low")
    deadline: Optional[str] = Field(description="截止時間，格式：YYYY-MM-DD")
    estimated_hours: float = Field(description="預估工時", ge=0)
    
    @validator('priority')
    def validate_priority(cls, v):
        if v not in ['high', 'medium', 'low']:
            raise ValueError('優先級必須是 high, medium, low 其中之一')
        return v

# 使用範例
parser = PydanticOutputParser(pydantic_object=TaskExtraction)
prompt = PromptTemplate(
    template="從以下文本提取任務資訊：{text}\n{format_instructions}",
    input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = prompt | llm | parser
result = chain.invoke({"text": "需要在本週五前完成網站設計，預估需要 8 小時，這是高優先級任務"})
print(f"任務：{result.tasks}")
print(f"優先級：{result.priority}")
print(f"截止時間：{result.deadline}")
```

### 2. JSON Output Parser
**輕量級 JSON 結構輸出**

```python
from langchain_core.output_parsers import JsonOutputParser

json_parser = JsonOutputParser()
prompt = PromptTemplate(
    template="分析以下內容並以 JSON 格式返回：{text}\n請包含：sentiment, keywords, summary",
    input_variables=["text"]
)

chain = prompt | llm | json_parser
result = chain.invoke({"text": "AI技術發展迅速，未來前景看好"})
# result 是dict 格式
print(result["sentiment"])  # "positive"
print(result["keywords"])   # ["AI", "技術", "發展"]
```

### 3. Structured Output Parser
**基於 Response Schema 的結構化輸出**

```python
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

response_schemas = [
    ResponseSchema(name="product_name", description="產品名稱"),
    ResponseSchema(name="price", description="價格（數字）"),
    ResponseSchema(name="features", description="主要特色清單"),
    ResponseSchema(name="recommendation", description="是否推薦（true/false）")
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = parser.get_format_instructions()

prompt = PromptTemplate(
    template="分析以下產品資訊：{product_info}\n{format_instructions}",
    input_variables=["product_info"],
    partial_variables={"format_instructions": format_instructions}
)

chain = prompt | llm | parser
result = chain.invoke({"product_info": "iPhone 15 Pro，售價 NT$35,900，具備 A17 Pro 晶片和鈦金屬機身"})
print(result)  # 結構化字典輸出
```

### 4. Enum Output Parser
**枚舉類型輸出**

```python
from langchain_core.output_parsers import EnumOutputParser
from enum import Enum

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

parser = EnumOutputParser(enum=Priority)
prompt = PromptTemplate(
    template="評估以下任務的優先級：{task}\n{instructions}",
    input_variables=["task"],
    partial_variables={"instructions": parser.get_format_instructions()}
)

chain = prompt | llm | parser
result = chain.invoke({"task": "修復生產環境的緊急 bug"})
print(result)  # Priority.HIGH
print(result.value)  # "high"
```

## 進階輸出解析技術

### 1. 自定義輸出解析器

```python
from langchain_core.output_parsers import BaseOutputParser
from typing import List
import re

class EmailExtractorParser(BaseOutputParser[List[str]]):
    """自定義郵件地址提取器"""
    
    def parse(self, text: str) -> List[str]:
        # 使用正則表達式提取郵件地址
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))  # 去重
    
    @property
    def _type(self) -> str:
        return "email_extractor"

# 使用自定義解析器
parser = EmailExtractorParser()
chain = prompt | llm | parser
emails = chain.invoke({"text": "請聯絡 john@example.com 或 mary@company.org"})
print(emails)  # ['john@example.com', 'mary@company.org']
```

### 2. 錯誤處理與重試機制

```python
from langchain_core.output_parsers import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser

# 原始解析器
base_parser = PydanticOutputParser(pydantic_object=TaskExtraction)

# 包裝錯誤修復解析器
fixing_parser = OutputFixingParser.from_llm(
    parser=base_parser,
    llm=ChatOpenAI(model="gpt-4o-mini")
)

# 當原始解析失敗時，會使用 LLM 修復輸出格式
chain = prompt | llm | fixing_parser
result = chain.invoke({"text": "完成報告，很重要"})  # 即使輸出格式不完美也能解析
```

### 3. 多步驟解析管道

```python
# 複雜的多步驟解析流程
from langchain_core.runnables import RunnablePassthrough

# 第一步：基本資訊提取
basic_parser = PydanticOutputParser(pydantic_object=BasicInfo)

# 第二步：詳細分析
detailed_parser = PydanticOutputParser(pydantic_object=DetailedAnalysis)

# 組合解析管道
analysis_chain = {
    "basic": basic_prompt | llm | basic_parser,
    "original": RunnablePassthrough()
} | detailed_prompt | llm | detailed_parser

result = analysis_chain.invoke({"input_text": "分析對象"})
```

## 最佳實踐建議

### 1. 選擇合適的解析器

| 使用場景 | 推薦解析器 | 優勢 |
|----------|------------|------|
| **複雜業務邏輯** | PydanticOutputParser | 類型安全、驗證完整、IDE 支援 |
| **簡單 JSON 輸出** | JsonOutputParser | 輕量級、快速 |
| **固定欄位結構** | StructuredOutputParser | 配置簡單、向後相容 |
| **枚舉選擇** | EnumOutputParser | 類型安全、選項限制 |
| **特殊格式** | 自定義 Parser | 完全客製化 |

### 2. 錯誤處理策略

```python
# 🔒 堅固的錯誤處理
class RobustParsingChain:
    def __init__(self, primary_parser, fallback_parser=None):
        self.primary_parser = primary_parser
        self.fallback_parser = fallback_parser or StrOutputParser()
    
    def parse_with_fallback(self, llm_output):
        try:
            return self.primary_parser.parse(llm_output)
        except Exception as e:
            logger.warning(f"主解析器失敗：{e}，使用備用解析器")
            return self.fallback_parser.parse(llm_output)

# 使用範例
robust_parser = RobustParsingChain(
    primary_parser=PydanticOutputParser(pydantic_object=MyModel),
    fallback_parser=StrOutputParser()
)
```

### 3. 性能優化

```python
# 🚀 快取解析指示
from functools import lru_cache

class CachedParser(PydanticOutputParser):
    @lru_cache(maxsize=128)
    def get_format_instructions(self):
        return super().get_format_instructions()

# 批量解析優化
def batch_parse(texts: List[str], parser):
    """批量解析，提高效率"""
    chain = prompt | llm | parser
    return chain.batch([{"text": text} for text in texts])
```

### 4. 與 LCEL 整合

```python
# 在 LCEL 鏈中使用結構化輸出
from langchain_core.runnables import RunnableParallel

# 並行解析多種格式
multi_format_chain = RunnableParallel({
    "structured": prompt | llm | pydantic_parser,
    "json": prompt | llm | json_parser,
    "enum": priority_prompt | llm | enum_parser
})

results = multi_format_chain.invoke({"text": "輸入文本"})
```

## 實際應用範例

### 智能表單填寫系統

```python
class FormData(BaseModel):
    name: str = Field(description="姓名")
    email: str = Field(description="郵件地址")
    phone: Optional[str] = Field(description="電話號碼")
    age: int = Field(description="年齡", ge=0, le=150)
    interests: List[str] = Field(description="興趣愛好")
    
form_parser = PydanticOutputParser(pydantic_object=FormData)
form_prompt = PromptTemplate(
    template="從以下對話中提取表單資訊：{conversation}\n{format_instructions}",
    input_variables=["conversation"],
    partial_variables={"format_instructions": form_parser.get_format_instructions()}
)

form_chain = form_prompt | llm | form_parser

conversation = """
用戶: 你好，我叫張小明，今年28歲
客服: 您好！請問您的聯絡方式？
用戶: 我的郵箱是zhangxm@email.com，手機是0912345678
客服: 您有什麼興趣愛好嗎？
用戶: 我喜歡攝影、旅遊和閱讀
"""

form_data = form_chain.invoke({"conversation": conversation})
print(f"姓名: {form_data.name}")
print(f"年齡: {form_data.age}")
print(f"郵箱: {form_data.email}")
print(f"興趣: {', '.join(form_data.interests)}")
```

### 智能合約條款解析

```python
class ContractClause(BaseModel):
    clause_type: str = Field(description="條款類型：payment, delivery, warranty, penalty")
    description: str = Field(description="條款描述")
    key_terms: List[str] = Field(description="關鍵條件")
    risk_level: str = Field(description="風險等級：low, medium, high")

contract_parser = PydanticOutputParser(pydantic_object=ContractClause)
contract_chain = contract_prompt | legal_llm | contract_parser

contract_text = """
第五條 付款條款：買方應在收到貨物後30天內付清全款，逾期每日按欠款金額的0.05%計收滯納金。
如超過60天未付款，賣方有權收回貨物並追究違約責任。
"""

clause = contract_chain.invoke({"text": contract_text})
print(f"條款類型: {clause.clause_type}")
print(f"風險等級: {clause.risk_level}")
print(f"關鍵條件: {clause.key_terms}")
```

## 總結

結構化輸出解析器是 LangChain 中確保資料品質和類型安全的關鍵組件：

- 🎯 **精確控制** - 定義明確的輸出格式和驗證規則
- 🛡️ **類型安全** - Pydantic 模型提供完整的類型檢查
- 🔄 **錯誤恢復** - 內建重試和修復機制
- ⚡ **高效處理** - 支援批量和異步處理
- 🔧 **易於整合** - 與 LCEL 無縫結合
- 📊 **多格式支援** - JSON、枚舉、自定義格式

選擇合適的解析器類型，結合良好的錯誤處理策略，能夠大大提升 AI 應用的可靠性和可維護性。

---

::: tip 下一步
現在你已經掌握了結構化輸出解析，接下來可以：
1. [記憶機制與對話管理](/tutorials/memory-systems) - 結合結構化輸出建構智能對話
2. [監控與可觀測性](/tutorials/monitoring) - 監控解析器的性能和準確性
3. [進階應用案例](/tutorials/advanced-examples) - 查看企業級的解析器應用
:::

::: warning 開發建議
- **謹慎設計 Schema**：清晰的欄位描述有助於提高解析準確性
- **充分測試**：為不同的輸入情況編寫測試用例
- **錯誤處理**：始終準備備用解析策略
- **性能監控**：追蹤解析成功率和執行時間
:::
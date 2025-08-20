# LangChain Prompt Template 教學

在開發 LLM（Large Language Model）應用時，最常見的需求就是「設計提示詞」（Prompt）。
一開始我們可能會直接用字串拼接，但隨著應用規模變大，這種方式會變得難以維護。
這時候 **LangChain 的 PromptTemplate** 就能派上用場。

---

## 為什麼不用 f-string？

我們先看看最傳統的做法：

```python
# 定義程式語言變數
language = "Python"

# 使用 f-string 進行字串格式化
prompt = f"What is the best way to learn coding in {language}?"

# 印出結果
print(prompt)
```

👉 輸出：

```
What is the best way to learn coding in Python?
```

雖然 f-string 很直覺，但存在幾個問題：

1. **維護困難**：當專案大了，Prompt 會散落在程式各處，很難管理。
2. **沒有驗證機制**：如果少傳一個變數，程式就會報錯。
3. **難以組合**：不同情境下的 Prompt 要自己手動拼接。
4. **無法分享**：f-string 只能寫在程式碼裡，沒辦法輕易存成檔案共用。

---

## LangChain PromptTemplate

LangChain 提供了一個更結構化的方式：

```python
# 匯入 LangChain 的 PromptTemplate 類別
from langchain.prompts import PromptTemplate

# 定義提示詞模板字串
# 使用 {變數名} 作為佔位符，稍後可以動態替換
template = """你是一個專業醫師，請根據以下資訊提供建議：
症狀: {symptom}
病史: {history}
請以簡單明瞭的方式回答。"""

# 從模板字串建立 PromptTemplate 物件
# from_template() 會自動解析 {} 中的變數名稱
prompt_template = PromptTemplate.from_template(template)

# 使用 format() 方法傳入實際的參數值
# symptom 和 history 必須與模板中的變數名稱完全一致
final_prompt = prompt_template.format(
    symptom="頭痛", 
    history="有高血壓病史"
)

# 印出最終組合好的提示詞
print(final_prompt)
```

👉 輸出：

```
你是一個專業醫師，請根據以下資訊提供建議：
症狀: 頭痛
病史: 有高血壓病史
請以簡單明瞭的方式回答。
```

---

## f-string vs PromptTemplate

| 特點                            | f-string | PromptTemplate     |
| ----------------------------- | -------- | ------------------ |
| **簡單拼字串**                     | ✅        | ✅                  |
| **錯誤檢查**                      | ❌ 沒有檢查   | ✅ 驗證缺少參數           |
| **可重複使用**                     | ❌ 難共用    | ✅ 可存成 `.json/.yml` |
| **可組合性**                      | ❌ 自己拼接   | ✅ 模組化組合            |
| **進階功能 (few-shot, selector)** | ❌        | ✅ 支援               |

---

## 優勢總結

使用 **LangChain PromptTemplate** 可以讓你：

* **驗證輸入參數** → 避免因缺少變數而報錯。
* **組合多個 Prompt** → 輕鬆建立複雜的提示。
* **插入範例 (k-shot examples)** → 讓模型更精準回答。
* **存取外部檔案** → 支援 `.yml` 和 `.json`，方便多人協作。
* **自訂邏輯** → 可以擴展成更強大的客製化模板。

---

## 適用場景

* **小測試、一次性需求** → f-string 足夠。
* **正式專案、多情境應用** → 使用 PromptTemplate，更安全、更可維護。

---

# 進階：把 PromptTemplate 用到專案級

## A. 動態 few‑shot：自動挑範例插入（Example Selector）

當問題多變時，不可能手動維護所有 few‑shot 例子。**Example Selector** 可以依「目前輸入」自動挑選最合適的範例插入到提示中。

這裡示範兩種 Selector：

* **LengthBasedExampleSelector**：控制例子總長度（不需向量庫，最穩）
* **SemanticSimilarityExampleSelector**：語義相似度挑例（需 embeddings/vectorstore）

### A-1. 不依賴外部服務：LengthBasedExampleSelector

```python
# 匯入必要的 LangChain 組件
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector

# 定義 few-shot 範例集（實際專案中可以從資料庫或檔案讀取）
# 每個範例都包含輸入（symptom, history）和預期輸出（advice）
examples = [
    {
        "symptom": "頭痛", 
        "history": "高血壓", 
        "advice": "補充水分、避免咖啡因，必要時就醫檢查血壓。"
    },
    {
        "symptom": "喉嚨痛", 
        "history": "無", 
        "advice": "多喝溫水、避免刺激性食物，若>3天未改善再就醫。"
    },
    {
        "symptom": "胸悶", 
        "history": "家族心臟病史", 
        "advice": "立即評估心血管風險，若伴隨出汗/噁心請急診。"
    },
    {
        "symptom": "腹瀉", 
        "history": "近期出國", 
        "advice": "補充電解質，注意飲食衛生，症狀加劇需就醫。"
    },
]

# 定義單個範例的渲染格式
# 這個模板會用於格式化每一個 few-shot 範例
example_prompt = PromptTemplate(
    input_variables=["symptom", "history", "advice"],  # 必須與 examples 中的 key 名稱一致
    template="症狀: {symptom}\n病史: {history}\n建議: {advice}\n"  # \n 為換行字元
)

# 建立基於長度的範例選擇器
# 這個選擇器會根據 token 長度限制來選擇範例
selector = LengthBasedExampleSelector(
    examples=examples,                    # 傳入所有可用的範例
    example_prompt=example_prompt,        # 範例的格式化模板
    max_length=200                        # 最大允許的範例總長度（字元數）
    # 如果所有範例超過這個長度，會自動減少範例數量
)

# 建立完整的 few-shot 提示詞模板
few_shot_prompt = FewShotPromptTemplate(
    example_selector=selector,             # 使用上面定義的選擇器
    example_prompt=example_prompt,         # 單個範例的格式模板
    prefix=(
        # 範例之前的前置說明（定義 AI 的角色和範例的目的）
        "你是一位專業醫療助理。以下是過去高品質的回答範例：\n"
    ),
    suffix=(
        # 範例之後的後置說明（包含使用者的實際問題）
        "請根據使用者目前的資訊提供建議：\n"
        "目前症狀: {symptom}\n"      # 這些變數會在執行時被替換
        "病史: {history}\n"
        "請給出清楚、分點、可行的建議。"
    ),
    input_variables=["symptom", "history"]  # suffix 中使用的變數名稱
)

# 使用模板生成最終的提示詞
# 系統會自動：
# 1. 使用 selector 選擇適合的範例
# 2. 用 example_prompt 格式化選中的範例
# 3. 組合 prefix + 範例 + suffix
rendered = few_shot_prompt.format(
    symptom="咳嗽、痰多",  # 使用者的症狀
    history="過敏史"         # 使用者的病史
)

# 印出最終的提示詞（這就是會送給 LLM 的內容）
print(rendered)
```

### A-2. 語義相似度挑例（需要向量庫）

> 適合例子很多、需要「語意相近」範例時使用。

```python
# 注意：這個範例需要安裝額外的依賴套件
# pip install faiss-cpu langchain-community sentence-transformers

# 匯入語義相似度範例選擇器所需的模組
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_community.vectorstores import FAISS  # Facebook AI 相似性搜尋向量資料庫
from langchain_community.embeddings import HuggingFaceEmbeddings  # Hugging Face 嵌入模型
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector

# 定義訓練範例集（實際應用中範例數量會更多，增加選擇的精確度）
examples = [
    {
        "symptom": "頭痛", 
        "history": "高血壓", 
        "advice": "補水與血壓監測，避免壓力過大"
    },
    {
        "symptom": "胸悶", 
        "history": "家族心臟病史", 
        "advice": "心血管風險評估，建議心電圖檢查"
    },
    {
        "symptom": "喉嚨痛", 
        "history": "無", 
        "advice": "休息與保暖，多喝溫開水"
    },
    {
        "symptom": "腹瀉", 
        "history": "近期出國", 
        "advice": "電解質補充，注意食物安全"
    },
]

# 定義範例格式化模板（與前面的例子相同）
example_prompt = PromptTemplate(
    input_variables=["symptom", "history", "advice"],
    template="症狀: {symptom}\n病史: {history}\n建議: {advice}\n"
)

# 初始化嵌入模型（將文字轉換為向量表示）
# all-MiniLM-L6-v2 是一個輕量且效果不錯的多語言模型
emb = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 建立語義相似度範例選擇器
# 這會自動將所有範例轉換為向量並建立搜尋索引
selector = SemanticSimilarityExampleSelector.from_examples(
    examples=examples,                    # 所有可選的範例
    embeddings=emb,                      # 用於計算文字相似度的嵌入模型
    vectorstore_cls=FAISS,               # 向量資料庫類別（用於高效搜尋）
    k=2,                                 # 每次選擇最相似的 2 個範例
    input_keys=["symptom", "history"]    # 用於計算相似度的輸入欄位
    # 系統會將使用者的 symptom + history 與範例進行語義比對
)

# 建立使用語義選擇器的 few-shot 模板
few_shot_prompt = FewShotPromptTemplate(
    example_selector=selector,            # 使用智能選擇器（而非固定範例）
    example_prompt=example_prompt,        # 範例格式化模板
    prefix="你是一位專業醫療助理。以下是相似案例的範例：\n",  # 前置說明
    suffix=(
        "目前症狀: {symptom}\n"           # 使用者的實際問題
        "病史: {history}\n"
        "請以要點方式提出建議。"
    ),
    input_variables=["symptom", "history"]  # 使用者需要提供的變數
)

# 測試語義相似度選擇
# 系統會自動找出與「胸口悶痛、呼吸急促 + 抽菸多年」最相似的範例
rendered_prompt = few_shot_prompt.format(
    symptom="胸口悶痛、呼吸急促", 
    history="抽菸多年"
)

# 印出結果（應該會選擇與心血管相關的範例）
print(rendered_prompt)
```

---

## B. 可組合聊天模板 + LCEL：system/human 分層，串接到模型

在聊天任務中，我們常把**規則**（system）與**使用者問題**（human）分開，最後用 **LCEL 管線** 直接接到模型。

```python
# 注意：若要實際呼叫模型需要安裝對應套件
# pip install langchain-core langchain-openai

# 匯入聊天模板和輸出解析器
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# 若要使用 OpenAI 模型，需要匯入：
# from langchain_openai import ChatOpenAI

# 1) 建立聊天模板，分為 system 和 human 角色
# system: 定義 AI 的身份、規則和行為準則
# human: 包含使用者的實際問題和相關資訊
chat_prompt = ChatPromptTemplate.from_messages([
    (
        "system",  # 系統角色訊息
        "你是專業醫療助理。回答需要遵循以下原則：\n"
        "1) 提供明確分點的建議\n"
        "2) 優先考慮安全性\n"
        "3) 不進行診斷，僅給予一般性建議\n"
        "4) 建議嚴重症狀時立即就醫"
    ),
    (
        "human",   # 使用者角色訊息
        "症狀: {symptom}\n"      # 使用者輸入的症狀
        "病史: {history}\n"      # 使用者的相關病史
        "困擾: {question}"       # 使用者的具體問題
    )
])

# 2) 可選：整合 few-shot 範例到聊天模板中
# 如果你已經有 few-shot 範例（如前面 A 部分生成的），可以這樣加入：
# few_shot_examples = "範例1: ...\n範例2: ..."  # 從前面的 FewShotPromptTemplate 取得
# enhanced_chat_prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是專業醫療助理..."),
#     ("system", few_shot_examples),  # 加入範例作為額外的系統指令
#     ("human", "症狀: {symptom}...")
# ])

# 3) 建立 LCEL (LangChain Expression Language) 處理鏈
# 這個管線會依序執行：提示詞模板 → 模型 → 輸出解析器
# model = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # 初始化語言模型
# chain = chat_prompt | model | StrOutputParser()          # 建立處理鏈
# 注意：| 符號是 LCEL 的管線運算子，用於串接不同的處理步驟

# 4) 執行完整的處理鏈（需要有效的 API 金鑰）
# result = chain.invoke({
#     "symptom": "胸悶", 
#     "history": "家族心臟病史", 
#     "question": "是否需要立刻就醫？"
# })
# print("AI 回應:", result)

# 5) 僅預覽提示詞內容（不呼叫模型）
# 這對於偵錯和驗證提示詞格式很有用
print("=== 預覽聊天訊息格式 ===")
rendered_msgs = chat_prompt.format_messages(
    symptom="胸悶",           # 使用者的症狀
    history="家族心臟病史",    # 使用者的病史
    question="是否需要立刻就醫？"  # 使用者的問題
)

# 遍歷並顯示每個訊息的角色和內容
for message in rendered_msgs:
    print(f"[{message.type}] {message.content}")
    print("-" * 40)
```

**重點優勢**

* **結構清晰**：system/human/（可選）assistant樣例，各司其職。
* **容易組裝**：few‑shot 片段可作為 system 的附加規範或 human 的提示補充。
* **可測試**：可先 `format_messages()` 檢查內容，再接模型，避免線上出錯。

---

## C. 外部化與重用：把 Prompt 存成 YAML / JSON

多人協作時，**把 Prompt 從程式碼抽離**很重要。你可以用 LangChain 的序列化能力把模板存成檔案，統一管理。

### C-1. 存成 YAML

```python
# 匯入 PromptTemplate 類別
from langchain.prompts import PromptTemplate
import os

# 建立一個簡單的提示詞模板
template = PromptTemplate.from_template(
    "請以{tone}口吻，將以下症狀提供三點建議：{symptom}"
)

# 確保目錄存在（實務上建議使用統一的檔案管理系統）
os.makedirs("prompts", exist_ok=True)

# 儲存模板到 YAML 檔案
# LangChain 會自動序列化模板的所有資訊
template.save("prompts/advise_prompt.yaml")

# 也可以儲存為 JSON 格式
# template.save("prompts/advise_prompt.json")

print("模板已儲存到 prompts/advise_prompt.yaml")
```

> 產出的 YAML 會包含 prompt 類型、模板字串、輸入變數等資訊。

### C-2. 從檔案載入

```python
# 匯入模板載入函式
from langchain.prompts import load_prompt

# 從 YAML 檔案載入之前儲存的模板
# LangChain 會自動反序列化所有必要的資訊
loaded_template = load_prompt("prompts/advise_prompt.yaml")

# 驗證載入的模板類型和變數
print(f"模板類型: {type(loaded_template)}")
print(f"輸入變數: {loaded_template.input_variables}")
print(f"模板內容: {loaded_template.template}")
print("-" * 50)

# 使用載入的模板生成提示詞
result = loaded_template.format(
    tone="專業且同理",          # 回答的語氣風格
    symptom="長期咳嗽與喉嚨痛"  # 使用者的症狀
)

print("最終生成的提示詞:")
print(result)
```

**搭配做法**

* 由 **內容策展/醫務顧問** 在 YAML 中維護措辭與規範；
* 由 **工程師** 在程式管理資料流與變數映射；
* CI 中可加入 **lint/審核**（例如字數、敏感詞、禁語）。

---

## D. 輸入驗證與「預填」（partial）

當某些欄位固定或需預設值時，可用 **partial** 先綁定，並保留其他變數在執行時填入；同時，缺少必要輸入會在 `format()` 時拋錯，**提早暴露問題**。

```python
# 匯入 PromptTemplate 類別
from langchain.prompts import PromptTemplate

# 建立包含多個變數的基礎模板
base_template = PromptTemplate.from_template(
    "【口吻:{tone}】症狀:{symptom}，請提供三點建議。"
)

# 檢視原始模板的輸入變數
print(f"原始模板需要的變數: {base_template.input_variables}")
print(f"原始模板內容: {base_template.template}")
print("-" * 50)

# 使用 partial() 方法預先綁定某些變數
# 這在以下情況很有用：
# 1. 某些變數在整個應用中都是固定的
# 2. 想要建立專門化的模板版本
# 3. 減少呼叫時需要傳遞的參數數量
professional_prompt = base_template.partial(
    tone="專業、同理、可執行"  # 預先設定回答的語氣風格
)

# 檢視 partial 後的模板變化
print(f"預填後的模板需要的變數: {professional_prompt.input_variables}")
print(f"預填後的模板: {professional_prompt}")
print("-" * 50)

# 現在只需要提供 symptom 變數即可
# 如果忘記提供必要的變數，會在執行時拋出 KeyError
try:
    # 正確使用：提供所有必要的變數
    result = professional_prompt.format(symptom="胸悶與頭暈")
    print("✅ 成功生成提示詞:")
    print(result)
    print("-" * 50)
    
    # 錯誤示範：缺少必要變數（這會拋出錯誤）
    # incomplete_result = professional_prompt.format()  # 缺少 symptom 變數
    
except KeyError as e:
    print(f"❌ 錯誤：缺少必要的變數 {e}")

# partial 的進階應用：動態預填
def create_specialized_prompt(specialty):
    """根據專科建立專門化的提示詞模板"""
    base = PromptTemplate.from_template(
        "你是{specialty}專科醫師。症狀：{symptom}，病史：{history}，請給予專業建議。"
    )
    return base.partial(specialty=specialty)

# 建立不同專科的模板
cardiology_prompt = create_specialized_prompt("心臟內科")
neurology_prompt = create_specialized_prompt("神經內科")

# 使用專科模板
heart_advice = cardiology_prompt.format(
    symptom="胸悶、心悸", 
    history="高血壓家族史"
)
print("心臟科建議:")
print(heart_advice)
```

---

## E. 把 A～D 串起來的實戰心法

1. **先寫死 → 抽模板 → few‑shot → selector**
   先用 f‑string 驗概念，成形後抽到 PromptTemplate；若回答不穩定，再加 few‑shot；範例多時導入 selector。

2. **可觀測性**
   在送模型前，**一律先 `format()` / `format_messages()` 檢查**，確保模板與資料對齊，減少線上 debug。

3. **外部化治理**
   把模板 YAML 化，交由內容策展與法遵/醫務團隊審閱；程式只負責注入資料與串接模型。

4. **資源預算**
   few‑shot 會增加 tokens；以 **LengthBasedExampleSelector** 或 **k 值**控管成本，必要時對範例做「壓縮/摘要」。
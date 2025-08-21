# 教學課程

歡迎來到 LangChain 教學課程！這裡提供完整的學習路徑，從基礎概念到進階應用，幫助您成為 LangChain 開發專家。

## 🎯 學習路徑

### 📚 基礎教學

建議按照以下順序學習基礎概念：

<div class="course-grid">

::: tip 1. LangChain 介紹
[開始學習 →](/tutorials/introduction)

了解 LangChain 是什麼、核心理念和實際應用
- 增強資料感知概念
- 增強行動力設計
- 實際應用場景與安全開發
:::

::: tip 2. 環境設置
[開始學習 →](/tutorials/setup)

準備 LangChain 開發環境
- Python 環境配置
- 套件安裝與管理
- API 金鑰設定
:::

::: tip 3. 免費 LLM 模型指南
[開始學習 →](/tutorials/free-llm-models)

學習使用免費的開源模型
- Ollama 本地模型部署
- Hugging Face 模型整合
- 模型選擇與比較
:::

::: tip 4. 第一個應用
[開始學習 →](/tutorials/first-app)

動手建構第一個 LangChain 應用程式
- 基本聊天機器人
- Prompt 模板使用
- 錯誤處理最佳實踐
:::

::: tip 5. Chat Models 對話模型
[開始學習 →](/tutorials/chat-models)

理解現代 AI 對話模型的核心概念
- SystemMessage/HumanMessage/AIMessage
- 多輪對話與上下文管理
- LangChain 0.3+ 最新功能
:::

::: tip 6. Prompt Template 提示範本
[開始學習 →](/tutorials/prompt-template)

掌握提示範本設計與變數管理
- 動態提示生成
- 範本組合與重用
- 最佳實踐模式
:::

</div>

### ⚡ 核心技術

掌握基礎後，深入學習 LangChain v0.2+ 的核心技術：

<div class="course-grid">

::: info 7. 結構化輸出解析
[開始學習 →](/tutorials/output-parsers)

確保 AI 輸出的結構化和類型安全
- Pydantic 模型驗證
- JSON 和枚舉解析器
- 錯誤處理與重試機制
:::

::: info 8. LCEL 表達式語言
[開始學習 →](/tutorials/lcel)

LangChain Expression Language 深度解析
- 管道操作符與鏈式組合
- RunnableParallel 並行處理
- 條件分支與動態路由
:::

::: info 9. Streaming Chat Models 串流對話模型
[開始學習 →](/tutorials/streaming-chat-models)

掌握串流聊天模型的完整實作
- 串流 vs 非串流差異分析
- 工程實務與最佳實踐
- 三大供應商（OpenAI/Claude/Gemini）比較
:::

::: info 10. 批次請求與非同步函式
[開始學習 →](/tutorials/multiple-llm-generations)

高效能多回應生成技術
- .batch() 批次處理
- 非同步 API (.abatch(), .ainvoke())
- 並行處理與效能優化
:::

::: info 11. 記憶系統 📝 撰寫中
[開始學習 →](/tutorials/memory)

基礎對話記憶管理
- 對話歷史保存
- 上下文管理
- 記憶類型選擇
:::

::: info 12. 記憶機制與對話管理 📝 撰寫中
[開始學習 →](/tutorials/memory-systems)

v0.2+ 進階記憶架構
- RunnableWithMessageHistory
- 多會話管理與持久化
- 智能記憶壓縮與檢索
:::

::: info 13. 模型整合 📝 撰寫中
[開始學習 →](/tutorials/model-integration)

深入了解各種 LLM 模型整合
- 多模型支援策略
- API 配置與優化
- 成本控制技巧
:::

</div>

### 🚀 進階應用

精通核心技術後，學習完整的應用建構：

<div class="course-grid">

::: info 14. LangChain 架構與核心概念
[開始學習 →](/tutorials/architecture)

深入了解框架架構與抽象化設計
- v0.2+ 現代架構解析
- LCEL/Runnables 與 LangGraph
- 抽象化概念與複雜功能
:::

::: info 15. RAG 應用 📝 撰寫中
[開始學習 →](/tutorials/rag)

建構檢索增強生成系統
- 向量資料庫整合
- 文件處理與分割
- 檢索策略優化
:::

::: info 16. LangGraph 工作流框架 📝 撰寫中
[開始學習 →](/tutorials/langgraph)

下一代智能代理工作流框架
- 狀態管理與節點設計
- 條件路由與循環控制
- 多代理協作與錯誤處理
:::

::: info 17. 監控與可觀測性 📝 撰寫中
[開始學習 →](/tutorials/monitoring)

LangSmith 整合與生產監控
- 執行追蹤與性能分析
- A/B 測試與評估框架
- 成本控制與告警系統
:::

::: info 18. 進階應用案例 📝 撰寫中
[開始學習 →](/tutorials/advanced-examples)

企業級應用實戰案例
- 智能助手系統架構
- 多模態客服平台
- 文檔處理工作流
:::

</div>

## 🎮 實作練習

### 互動式 Demo

邊學邊做，透過實際操作加深理解：

- [Gemini 基礎聊天](/demos/gemini-chat) - 體驗 Google Gemini 整合
- [免費模型展示](/demos/free-models) - 比較不同開源模型
- [更多 Demo 展示](/demos/) - 探索更多應用場景

### 實用範例

參考完整的應用程式範例：

- [聊天機器人](/examples/chatbot) - 完整的對話系統
- [文檔問答](/examples/document-qa) - RAG 應用實例
- [工具整合](/examples/tools) - Agent 和工具調用

## 📈 學習建議

### 🔰 初學者路徑 (2-3週)
1. **LangChain 介紹** - 理解核心理念與應用場景
2. **環境設置** - 準備開發環境
3. **免費 LLM 模型指南** - 無成本開始實驗
4. **Chat Models 對話模型** - 掌握現代 AI 對話基礎
5. **Prompt Template 提示範本** - 掌握提示設計
6. **Demo 展示** - 體驗不同功能
7. ⏳ **第一個應用** (撰寫中) - 動手實作

### 🎓 進階開發者路徑 (4-6週)
1. 完成**基礎教學** 1-6
2. **核心技術學習**：
   - **結構化輸出解析** - 確保資料品質
   - **LCEL 表達式語言** - 掌握現代鏈式組合
   - **Streaming Chat Models** - 即時互動實作
   - **批次請求與非同步函式** - 效能優化
   - **記憶機制與對話管理** - 實現智能對話
3. **進階應用**：
   - **LangGraph 工作流框架** - 建構複雜智能代理
   - **監控與可觀測性** - 生產環境最佳實踐

### 🏢 企業應用路徑
1. 完成**基礎教學**和**核心技術**
2. 深度學習 **LangChain 架構與核心概念**
3. 重點掌握 **LangGraph 工作流框架**
4. 學習 **監控與可觀測性**
5. 參考 **進階應用案例**
6. ⏳ 考慮 **RAG 應用** (撰寫中) 和生產部署

## 💡 學習小貼士

::: warning 學習建議
- **循序漸進**：按照推薦順序學習，每章都有前後關聯
- **動手實作**：理論結合實際操作，加深理解
- **參考官方文檔**：LangChain 快速發展，隨時查看 [官方文檔](https://python.langchain.com/)
:::

::: tip 實作技巧
- 先從免費模型開始實驗，降低學習成本
- 每學完一章就動手寫程式碼驗證
- 善用 Demo 展示來理解實際應用
- 遇到問題時查看範例程式碼
:::

## 📚 額外資源

### 官方資源
- [LangChain 官方文檔](https://python.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)  
- [LangSmith 平台](https://smith.langchain.com/)

### 社群資源
- [LangChain Discord](https://discord.gg/langchain)
- [官方 Twitter](https://twitter.com/langchainai)
- [YouTube 教學影片](https://www.youtube.com/@langchain)

---

準備好開始學習了嗎？從 [LangChain 介紹](/tutorials/introduction) 開始你的 AI 開發之旅！

<style>
.course-grid {
  display: grid;
  gap: 1rem;
  margin: 1.5rem 0;
}

@media (min-width: 768px) {
  .course-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.course-grid .tip,
.course-grid .info {
  margin: 0;
}
</style>
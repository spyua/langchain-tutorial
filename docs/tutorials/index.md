# 教學課程

歡迎來到 LangChain 教學課程！這裡提供完整的學習路徑，從基礎概念到進階應用，幫助您成為 LangChain 開發專家。

## 🎯 學習路徑

### 📚 基礎教學

建議按照以下順序學習基礎概念：

<div class="course-grid">

::: tip 1. LangChain 介紹
[開始學習 →](/tutorials/introduction)

了解 LangChain 是什麼、核心概念和架構設計
- 框架概述與核心理念
- 模組化抽象功能解析  
- 實際應用場景示例
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

</div>

### 🚀 進階教學

掌握基礎後，進入進階主題：

<div class="course-grid">

::: info 模型整合
[開始學習 →](/tutorials/model-integration)

深入了解各種 LLM 模型整合
- 多模型支援策略
- API 配置與優化
- 成本控制技巧
:::

::: info 記憶系統
[開始學習 →](/tutorials/memory)

實現對話記憶和上下文管理
- 不同記憶類型選擇
- 長期記憶存儲
- 記憶檢索策略
:::

::: info RAG 應用
[開始學習 →](/tutorials/rag)

建構檢索增強生成系統
- 向量資料庫整合
- 文件處理與分割
- 檢索策略優化
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

### 🔰 初學者路徑
1. **LangChain 介紹** - 理解基本概念
2. **免費 LLM 模型指南** - 無成本開始實驗
3. **第一個應用** - 動手實作
4. **Demo 展示** - 體驗不同功能

### 🎓 進階開發者路徑  
1. **環境設置** - 建立專業開發環境
2. **模型整合** - 掌握模型選擇策略
3. **記憶系統** - 實現複雜對話邏輯
4. **RAG 應用** - 建構知識庫系統

### 🏢 企業應用路徑
1. 完成基礎教學
2. 重點學習 **RAG 應用**
3. 參考 **實用範例**
4. 考慮部署和擴展性

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
# LangChain 教學網站

::: info 歡迎來到 LangChain 學習中心！
這裡提供完整的 LangChain 學習資源，從基礎概念到進階應用，幫助您快速掌握 AI 應用開發。
:::

## 🎯 學習目標

- 理解 LangChain 的核心概念
- 學會整合各種 AI 模型
- 建構實用的 AI 應用程式  
- 掌握最佳實踐方法

## 🚀 快速開始
- [📚 教學課程](/tutorials/) - 19個詳細教學，從基礎到進階
  - 基礎：介紹、設置、第一個應用、聊天模型
  - 進階：記憶系統、RAG、LangGraph、監控
  - 實戰：多模型整合、串流、架構模式
- [💼 實用範例](/examples/) - 真實應用場景示範
- [🎮 互動 Demo](/demos/) - Streamlit 實作體驗

## 🔧 技術特色

<div class="features">
<div class="feature">
  <h3>🔗 完整整合</h3>
  <p>支援多種 AI 模型，包括 OpenAI、Google Gemini、Anthropic Claude 等</p>
</div>

<div class="feature">
  <h3>📖 實用教學</h3>
  <p>從基礎到進階，提供完整的學習路徑和實作範例</p>
</div>

<div class="feature">
  <h3>🎮 互動 Demo</h3>
  <p>可執行的 Streamlit 應用，讓您親手體驗 LangChain 功能</p>
</div>
</div>

## 📋 環境需求

- Python 3.8+
- Streamlit (用於互動 Demo)
- LangChain
- 相關 AI 模型 API 金鑰

::: warning 注意事項
使用前請確保已取得相關 AI 服務的 API 金鑰，並妥善設置環境變數。
:::

## 🎯 建議學習順序

### 初學者路徑 (2-3週)
1. **📖 基礎概念** - [LangChain 介紹](/tutorials/introduction) → [環境設置](/tutorials/setup)
2. **🔧 核心功能** - [第一個應用](/tutorials/first-app) → [聊天模型](/tutorials/chat-models) → [提示範本](/tutorials/prompt-template)
3. **🎮 實作練習** - 體驗 [免費模型 Demo](/demos/free-models)

### 進階開發路徑 (4-6週)
4. **⚡ 進階特性** - [輸出解析器](/tutorials/output-parsers) → [LCEL](/tutorials/lcel) → [記憶系統](/tutorials/memory)
5. **🚀 實際應用** - [RAG 應用](/tutorials/rag) → [多模型整合](/tutorials/multiple-llm-generations)
6. **🏗️ 架構設計** - [LangGraph](/tutorials/langgraph) → [架構模式](/tutorials/architecture) → [監控](/tutorials/monitoring)

---

<style>
.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.feature {
  padding: 20px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
}

.feature h3 {
  margin-top: 0;
  color: var(--vp-c-brand-1);
}
</style>
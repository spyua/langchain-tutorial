import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(
  defineConfig({
    title: 'LangChain 教學網站',
    description: '學習如何使用 LangChain 建構 AI 應用程式',
    lang: 'zh-TW',
    base: '/langchain-tutorial/',
    
    // Mermaid 配置
    mermaid: {
      theme: 'default'
    },
    
    themeConfig: {
      nav: [
        { text: '首頁', link: '/' },
        { text: '教學課程', link: '/tutorials/' },
        { text: '實作範例', link: '/examples/' },
        { text: 'Demo 展示', link: '/demos/' }
      ],

      sidebar: {
        '/tutorials/': [
          {
            text: '📚 基礎教學',
            items: [
              { text: 'LangChain 介紹', link: '/tutorials/introduction' },
              { text: '環境設置', link: '/tutorials/setup' },
              { text: '免費 LLM 模型指南', link: '/tutorials/free-llm-models' },
              { text: '第一個應用', link: '/tutorials/first-app' },
              { text: 'Chat Models 對話模型', link: '/tutorials/chat-models' },
              { text: 'Prompt Template 提示範本', link: '/tutorials/prompt-template' }
            ]
          },
          {
            text: '⚡ 核心技術',
            items: [
              { text: '結構化輸出解析', link: '/tutorials/output-parsers' },
              { text: 'LCEL 表達式語言', link: '/tutorials/lcel' },
              { text: 'Streaming Chat Models 串流對話模型', link: '/tutorials/streaming-chat-models' },
              { text: '批次請求與非同步函式', link: '/tutorials/multiple-llm-generations' },
              { text: '記憶系統 📝', link: '/tutorials/memory' },
              { text: '記憶機制與對話管理 📝', link: '/tutorials/memory-systems' },
              { text: '模型整合 📝', link: '/tutorials/model-integration' }
            ]
          },
          {
            text: '🚀 進階應用',
            items: [
              { text: 'LangChain 架構與核心概念', link: '/tutorials/architecture' },
              { text: 'RAG 應用 📝', link: '/tutorials/rag' },
              { text: 'LangGraph 工作流框架 📝', link: '/tutorials/langgraph' },
              { text: '監控與可觀測性 📝', link: '/tutorials/monitoring' },
              { text: '進階應用案例 📝', link: '/tutorials/advanced-examples' }
            ]
          }
        ],
        '/examples/': [
          {
            text: '實用範例',
            items: [
              { text: '聊天機器人', link: '/examples/chatbot' },
              { text: '文檔問答', link: '/examples/document-qa' },
              { text: '工具整合', link: '/examples/tools' }
            ]
          }
        ],
        '/demos/': [
          {
            text: '互動展示',
            items: [
              { text: 'Gemini 基礎聊天', link: '/demos/gemini-chat' },
              { text: '免費模型展示', link: '/demos/free-models' },
              { text: '執行說明', link: '/demos/how-to-run' }
            ]
          }
        ]
      },

      socialLinks: [
        { icon: 'github', link: 'https://github.com/your-username/langchain-tutorial' }
      ],

      footer: {
        message: '使用 VitePress 建構的 LangChain 教學網站',
        copyright: 'Copyright © 2024'
      }
    }
  })
)
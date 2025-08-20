import streamlit as st
import os
from pathlib import Path

# 頁面設置
st.set_page_config(
    page_title="LangChain 教學網站",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 主標題
st.title("🔗 LangChain 教學網站")
st.markdown("### 學習如何使用 LangChain 建構 AI 應用程式")

# 側邊欄導航
with st.sidebar:
    st.header("📚 導航選單")
    
    section = st.selectbox(
        "選擇章節",
        ["首頁", "Demo 展示", "教學課程", "實用範例", "文檔資源"]
    )

# 首頁內容
if section == "首頁":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 歡迎來到 LangChain 教學網站！
        
        這裡提供完整的 LangChain 學習資源，從基礎概念到進階應用，幫助您快速掌握 AI 應用開發。
        
        ### 🎯 學習目標
        - 理解 LangChain 的核心概念
        - 學會整合各種 AI 模型
        - 建構實用的 AI 應用程式
        - 掌握最佳實踐方法
        
        ### 🚀 快速開始
        1. 選擇左側導航開始探索
        2. 從 Demo 展示開始體驗
        3. 跟隨教學課程深入學習
        4. 參考實用範例進行實作
        """)
    
    with col2:
        st.info("""
        💡 **提示**
        
        建議按照以下順序學習：
        1. Demo 展示
        2. 基礎教學
        3. 進階教學
        4. 實用範例
        """)

# Demo 展示
elif section == "Demo 展示":
    st.header("🎮 Demo 展示")
    
    demos = [
        {
            "title": "01. Gemini 基礎聊天",
            "description": "使用 LangChain 整合 Google Gemini API 的基礎聊天應用",
            "path": "streamlit-demos/01_gemini_basic",
            "features": ["API 連接測試", "多模型支援", "互動式聊天", "動態配置"]
        }
    ]
    
    for demo in demos:
        with st.expander(f"🔧 {demo['title']}", expanded=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(demo['description'])
                st.write("**功能特色:**")
                for feature in demo['features']:
                    st.write(f"- {feature}")
            
            with col2:
                demo_path = Path(demo['path'])
                if demo_path.exists():
                    st.success("✅ 可用")
                    if st.button(f"🚀 執行 {demo['title']}", key=demo['title']):
                        st.code(f"cd {demo['path']}\nstreamlit run gemini_chat.py", language="bash")
                    st.info("💡 在終端機執行上述命令來啟動 Demo")
                else:
                    st.error("❌ 路徑不存在")

# 教學課程
elif section == "教學課程":
    st.header("📖 教學課程")
    
    tab1, tab2 = st.tabs(["基礎教學", "進階教學"])
    
    with tab1:
        st.subheader("🌱 基礎教學")
        st.markdown("""
        ### 即將推出的課程：
        
        1. **LangChain 入門**
           - 什麼是 LangChain？
           - 安裝與設置
           - 第一個 LangChain 應用
        
        2. **模型整合**
           - 支援的模型類型
           - API 金鑰配置
           - 模型選擇最佳實踐
        
        3. **基礎聊天機器人**
           - 建構簡單聊天介面
           - 訊息處理
           - 回應格式化
        """)
    
    with tab2:
        st.subheader("🚀 進階教學")
        st.markdown("""
        ### 即將推出的課程：
        
        1. **記憶系統**
           - 對話記憶管理
           - 長期記憶存儲
           - 記憶檢索策略
        
        2. **工具整合**
           - 自定義工具開發
           - API 工具整合
           - 工具鏈組合
        
        3. **RAG 應用**
           - 文檔檢索系統
           - 向量資料庫整合
           - 知識庫問答
        """)

# 實用範例
elif section == "實用範例":
    st.header("💼 實用範例")
    st.info("更多實用範例正在開發中...")

# 文檔資源
elif section == "文檔資源":
    st.header("📚 文檔資源")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔗 官方資源")
        st.markdown("""
        - [LangChain 官方文檔](https://python.langchain.com/)
        - [LangChain GitHub](https://github.com/langchain-ai/langchain)
        - [LangSmith 平台](https://smith.langchain.com/)
        """)
    
    with col2:
        st.subheader("🛠️ 開發工具")
        st.markdown("""
        - [Streamlit 文檔](https://docs.streamlit.io/)
        - [Google AI Studio](https://aistudio.google.com/)
        - [OpenAI API](https://platform.openai.com/)
        """)

# 頁腳
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>🔗 LangChain 教學網站 - 讓 AI 應用開發變得簡單</div>",
    unsafe_allow_html=True
)
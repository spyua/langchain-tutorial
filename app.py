import streamlit as st
import os
import sys
from dotenv import load_dotenv

# 頁面設置
st.set_page_config(
    page_title="Gemini API 測試",
    page_icon="🤖",
    layout="wide"
)

# 載入環境變數
load_dotenv()

st.title("🤖 LangChain + Gemini API 測試")
st.write("簡化版本 - 確保基本功能正常")

# 顯示系統資訊
with st.expander("🔍 系統資訊"):
    st.write(f"**Python版本:** {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    st.write(f"**Streamlit版本:** {st.__version__}")
    st.write(f"**工作目錄:** {os.getcwd()}")
    
    # 檢查環境變數
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        st.success(f"✅ 找到API Key (前8字元: {api_key[:8]}...)")
    else:
        st.error("❌ 未找到GOOGLE_API_KEY環境變數")

# API Key輸入
st.header("🔧 API 設置")
api_key_input = st.text_input(
    "Google API Key", 
    value=os.getenv("GOOGLE_API_KEY", ""),
    type="password",
    help="請輸入你的Google API Key"
)

# 模型選擇
model_choice = st.selectbox(
    "選擇Gemini模型",
    ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"],
    index=0
)

st.write(f"**選擇的模型:** {model_choice}")

# 基本測試按鈕
if st.button("🧪 測試連接", type="primary"):
    if not api_key_input:
        st.error("請先輸入API Key")
    else:
        with st.spinner("正在測試連接..."):
            try:
                # 動態導入以避免啟動時錯誤
                from langchain_google_genai import ChatGoogleGenerativeAI
                from langchain.schema import HumanMessage, SystemMessage
                
                # 初始化模型
                llm = ChatGoogleGenerativeAI(
                    model=model_choice,
                    google_api_key=api_key_input,
                    temperature=0.7
                )
                
                # 簡單測試
                messages = [
                    SystemMessage(content="請簡短回答，用繁體中文。"),
                    HumanMessage(content="你好，請說'連接成功'")
                ]
                
                response = llm.invoke(messages)
                st.success("✅ 連接成功！")
                st.write(f"**Gemini回應:** {response.content}")
                
            except Exception as e:
                st.error(f"❌ 連接失敗: {str(e)}")

# 分隔線
st.markdown("---")

# 對話區域
st.header("💬 對話測試")

if api_key_input:
    user_question = st.text_area(
        "請輸入你的問題:",
        height=100,
        placeholder="例如: 請用繁體中文解釋什麼是機器學習"
    )
    
    if st.button("🚀 發送問題"):
        if user_question:
            with st.spinner("Gemini正在回答..."):
                try:
                    from langchain_google_genai import ChatGoogleGenerativeAI
                    from langchain.schema import HumanMessage, SystemMessage
                    
                    llm = ChatGoogleGenerativeAI(
                        model=model_choice,
                        google_api_key=api_key_input,
                        temperature=0.7
                    )
                    
                    messages = [
                        SystemMessage(content="你是一個有用的AI助手，請用繁體中文詳細回答問題。"),
                        HumanMessage(content=user_question)
                    ]
                    
                    response = llm.invoke(messages)
                    
                    # 顯示結果
                    st.markdown("### 🤖 Gemini的回答:")
                    st.write(response.content)
                    
                    # 顯示一些統計
                    st.markdown("### 📊 回答統計:")
                    st.write(f"- **字數:** {len(response.content)}")
                    st.write(f"- **使用模型:** {model_choice}")
                    
                except Exception as e:
                    st.error(f"❌ 發生錯誤: {str(e)}")
        else:
            st.warning("請先輸入問題")
else:
    st.info("請先在上方輸入API Key才能使用對話功能")

# 使用說明
with st.expander("📖 使用說明"):
    st.markdown("""
    ### 使用步驟:
    1. **檢查系統資訊** - 確保環境正常
    2. **輸入API Key** - 在上方輸入你的Google API Key
    3. **測試連接** - 點擊"測試連接"確保API正常
    4. **開始對話** - 在對話區域輸入問題
    
    ### 故障排除:
    - 如果連接失敗，檢查API Key是否正確
    - 確保網路連接正常
    - 檢查API配額是否足夠
    """)

# 頁腳
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>WSL2 環境中的 LangChain + Streamlit + Gemini 測試</div>",
    unsafe_allow_html=True
)
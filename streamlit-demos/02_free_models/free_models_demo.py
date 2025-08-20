"""
免費 LLM 模型示範應用
展示如何使用 Ollama 和 Hugging Face 的免費模型
"""

import streamlit as st
import os
from typing import Optional, List
import time

# 動態導入，避免在沒有安裝相依套件時出錯
try:
    from langchain_ollama import OllamaLLM
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from langchain_huggingface import HuggingFaceEndpoint
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

try:
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

def check_dependencies():
    """檢查必要的依賴是否已安裝"""
    missing_deps = []
    
    if not OLLAMA_AVAILABLE:
        missing_deps.append("langchain-ollama")
    if not HF_AVAILABLE:
        missing_deps.append("langchain-huggingface")
    if not LANGCHAIN_AVAILABLE:
        missing_deps.append("langchain-core")
    
    return missing_deps

def show_installation_guide(missing_deps: List[str]):
    """顯示安裝指南"""
    st.error("⚠️ 缺少必要的依賴套件")
    
    with st.expander("📦 安裝指南"):
        st.write("請在終端機中執行以下命令安裝缺少的套件：")
        
        install_cmd = "pip install " + " ".join(missing_deps)
        st.code(install_cmd, language="bash")
        
        st.write("或者安裝完整的依賴：")
        st.code("pip install langchain-ollama langchain-huggingface langchain-core", language="bash")

def test_ollama_connection() -> bool:
    """測試 Ollama 連接"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_available_ollama_models() -> List[str]:
    """獲取可用的 Ollama 模型"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
    except:
        pass
    return []

def create_ollama_llm(model_name: str) -> Optional[OllamaLLM]:
    """創建 Ollama LLM 實例"""
    try:
        return OllamaLLM(model=model_name, temperature=0.7)
    except Exception as e:
        st.error(f"創建 Ollama 模型時發生錯誤: {str(e)}")
        return None

def create_hf_llm(model_name: str, api_token: str = None) -> Optional[HuggingFaceEndpoint]:
    """創建 Hugging Face LLM 實例"""
    try:
        kwargs = {
            "repo_id": model_name,
            "model_kwargs": {"temperature": 0.7, "max_length": 200}
        }
        
        if api_token:
            kwargs["huggingfacehub_api_token"] = api_token
            
        return HuggingFaceEndpoint(**kwargs)
    except Exception as e:
        st.error(f"創建 Hugging Face 模型時發生錯誤: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="免費 LLM 模型示範",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 免費 LLM 模型示範")
    st.write("體驗不同的免費開源語言模型")
    
    # 檢查依賴
    missing_deps = check_dependencies()
    if missing_deps:
        show_installation_guide(missing_deps)
        return
    
    # 側邊欄配置
    st.sidebar.header("⚙️ 模型設定")
    
    model_type = st.sidebar.selectbox(
        "選擇模型類型",
        ["Ollama (本地模型)", "Hugging Face (託管模型)"]
    )
    
    if model_type == "Ollama (本地模型)":
        st.sidebar.subheader("Ollama 設定")
        
        # 檢查 Ollama 連接
        if test_ollama_connection():
            st.sidebar.success("✅ Ollama 服務運行中")
            
            # 獲取可用模型
            available_models = get_available_ollama_models()
            
            if available_models:
                selected_model = st.sidebar.selectbox(
                    "選擇模型",
                    available_models
                )
            else:
                st.sidebar.warning("沒有找到已下載的模型")
                st.sidebar.write("請先下載模型：")
                st.sidebar.code("ollama pull llama3.1", language="bash")
                selected_model = st.sidebar.text_input(
                    "或手動輸入模型名稱",
                    "llama3.1"
                )
        else:
            st.sidebar.error("❌ 無法連接到 Ollama 服務")
            with st.sidebar.expander("安裝 Ollama"):
                st.write("請先安裝並啟動 Ollama：")
                st.code("curl -fsSL https://ollama.com/install.sh | sh", language="bash")
                st.write("然後下載模型：")
                st.code("ollama pull llama3.1", language="bash")
            
            selected_model = st.sidebar.text_input(
                "模型名稱",
                "llama3.1"
            )
    
    else:  # Hugging Face
        st.sidebar.subheader("Hugging Face 設定")
        
        hf_models = [
            "google/flan-t5-small",
            "google/flan-t5-base", 
            "google/flan-t5-large",
            "microsoft/DialoGPT-small",
            "microsoft/DialoGPT-medium",
            "distilgpt2"
        ]
        
        selected_model = st.sidebar.selectbox(
            "選擇模型",
            hf_models
        )
        
        hf_token = st.sidebar.text_input(
            "Hugging Face API Token (選用)",
            type="password",
            help="提供 token 可以提高 API 限制"
        )
    
    # 主要內容區域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 對話測試")
        
        # 預設問題
        example_questions = [
            "你好，請介紹一下自己",
            "解釋什麼是人工智慧",
            "寫一個簡單的 Python 函數來計算斐波那契數列",
            "給我一些學習程式設計的建議",
            "什麼是機器學習？",
        ]
        
        # 問題選擇器
        question_type = st.radio(
            "選擇問題類型",
            ["預設問題", "自訂問題"],
            horizontal=True
        )
        
        if question_type == "預設問題":
            user_question = st.selectbox(
                "選擇一個問題",
                example_questions
            )
        else:
            user_question = st.text_area(
                "輸入你的問題",
                height=100,
                placeholder="在這裡輸入你的問題..."
            )
        
        # 執行按鈕
        if st.button("🚀 執行", type="primary"):
            if not user_question.strip():
                st.warning("請輸入問題")
                return
            
            # 創建模型實例
            if model_type == "Ollama (本地模型)":
                if not test_ollama_connection():
                    st.error("無法連接到 Ollama 服務，請確保 Ollama 正在運行")
                    return
                
                llm = create_ollama_llm(selected_model)
            else:
                llm = create_hf_llm(selected_model, hf_token)
            
            if llm is None:
                return
            
            # 顯示處理中
            with st.spinner(f"🤔 {selected_model} 正在思考..."):
                start_time = time.time()
                
                try:
                    # 執行推理
                    response = llm.invoke(user_question)
                    
                    end_time = time.time()
                    processing_time = end_time - start_time
                    
                    # 顯示結果
                    st.subheader("🤖 模型回應")
                    st.write(response)
                    
                    # 顯示性能指標
                    st.info(f"⏱️ 處理時間: {processing_time:.2f} 秒")
                    
                except Exception as e:
                    st.error(f"執行時發生錯誤: {str(e)}")
    
    with col2:
        st.subheader("📊 模型資訊")
        
        if model_type == "Ollama (本地模型)":
            st.write("**模型類型:** 本地運行")
            st.write(f"**模型名稱:** {selected_model}")
            st.write("**優點:**")
            st.write("- 完全免費")
            st.write("- 隱私安全") 
            st.write("- 離線使用")
            st.write("**需求:**")
            st.write("- 足夠的 RAM")
            st.write("- 本地儲存空間")
            
            if test_ollama_connection():
                st.success("✅ 服務狀態: 運行中")
            else:
                st.error("❌ 服務狀態: 未運行")
        else:
            st.write("**模型類型:** 託管服務")
            st.write(f"**模型名稱:** {selected_model}")
            st.write("**優點:**")
            st.write("- 無需本地資源")
            st.write("- 快速開始")
            st.write("- 多種模型選擇")
            st.write("**限制:**")
            st.write("- 需要網路連接")
            st.write("- API 使用限制")
            
            if hf_token:
                st.success("✅ API Token: 已設定")
            else:
                st.warning("⚠️ API Token: 未設定")
        
        # 使用說明
        with st.expander("📖 使用說明"):
            if model_type == "Ollama (本地模型)":
                st.write("**安裝 Ollama:**")
                st.code("curl -fsSL https://ollama.com/install.sh | sh")
                
                st.write("**下載模型:**")
                st.code("ollama pull llama3.1")
                
                st.write("**啟動服務:**")
                st.code("ollama serve")
            else:
                st.write("**獲取 API Token:**")
                st.write("1. 註冊 [Hugging Face](https://huggingface.co)")
                st.write("2. 前往 Settings > Access Tokens")
                st.write("3. 創建新的 token")
                st.write("4. 在左側輸入 token")
    
    # 底部資訊
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🔗 相關連結")
        st.write("- [Ollama 官網](https://ollama.com)")
        st.write("- [Hugging Face](https://huggingface.co)")
        st.write("- [LangChain 文檔](https://python.langchain.com)")
    
    with col2:
        st.subheader("💡 使用建議")
        st.write("- 本地模型適合隱私敏感應用")
        st.write("- 託管模型適合快速原型開發")
        st.write("- 根據硬體資源選擇模型大小")
    
    with col3:
        st.subheader("⚡ 效能優化")
        st.write("- 使用量化模型減少記憶體")
        st.write("- 調整 temperature 參數")
        st.write("- 批次處理提高效率")

if __name__ == "__main__":
    main()
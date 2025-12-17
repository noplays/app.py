import streamlit as st
import google.generativeai as genai

# --- 页面设置 ---
st.set_page_config(page_title="PA612 销售助手", page_icon="🤖")

st.title("🤖 尼龙销售 AI 助手")
st.write("你好！我是你的专属助手，请问有什么关于 PA612、PA610 或其他长碳链尼龙的问题？")

# --- 获取 API Key (安全的方式) ---
# 这里我们不直接写 Key，而是让它去读取云端的“保险箱”
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("还没有配置 API Key哦！请在 Streamlit 后台的 Secrets 里配置。")
    st.stop()

genai.configure(api_key=api_key)

# --- 模型设置 ---
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 聊天界面 ---
# 初始化聊天记录（这样你刷新网页记录不会丢）
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示之前的聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收用户输入
if prompt := st.chat_input("请输入你的问题..."):
    # 1. 显示用户的话
    with st.chat_message("user"):
        st.markdown(prompt)
    # 记录用户的话
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. 生成 AI 的回答
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            response = model.generate_content(prompt)
            full_response = response.text
            message_placeholder.markdown(full_response)
        except Exception as e:
            message_placeholder.markdown(f"出错了: {e}")
            full_response = f"出错了: {e}"
    
    # 记录 AI 的话
    st.session_state.messages.append({"role": "assistant", "content": full_response})

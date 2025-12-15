import streamlit as st
import openai  # DeepSeek兼容OpenAI SDK，直接用

# ====== DeepSeek 配置 ======
openai.api_key = st.secrets["DEEPSEEK_API_KEY"]
openai.base_url = "https://api.deepseek.com/v1"  # DeepSeek专属endpoint

st.set_page_config(page_title="TianYe's AI Chatbot", page_icon="🤖")

st.title("🤖 TianYe's AI Chatbot")
st.caption("Powered by DeepSeek Chat - Ask me anything! (支持中文)")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("What would you like to know? / 想问啥？"):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 调用DeepSeek
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = openai.chat.completions.create(
                model="deepseek-chat",  # 或 deepseek-coder，如果你想代码强
                messages=st.session_state.messages,
                temperature=0.7,
                stream=False
            )
        reply = response.choices[0].message.content
        st.markdown(reply)

    # 添加助手回复到历史
    st.session_state.messages.append({"role": "assistant", "content": reply})

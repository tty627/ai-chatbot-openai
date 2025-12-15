import streamlit as st
import openai

# ====== 配置你的OpenAI API Key ======
# 推荐用st.secrets方式（安全，不暴露key）
# 如果暂时没有secrets，先直接填你的key测试（上线前改secrets）
openai.api_key = st.secrets.get("OPENAI_API_KEY", "your-api-key-here")  # 先填你的key测试

st.set_page_config(page_title="TianYe's AI Chatbot", page_icon="🤖")

st.title("🤖 TianYe's AI Chatbot")
st.caption("Powered by OpenAI GPT - Ask me anything!")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# 显示历史消息
for message in st.session_state.messages[1:]:  # 跳过system
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("What would you like to know?"):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 调用OpenAI
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                temperature=0.7
            )
        reply = response.choices[0].message.content
        st.markdown(reply)

    # 添加助手回复到历史
    st.session_state.messages.append({"role": "assistant", "content": reply})

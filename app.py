import streamlit as st
import requests
import json
import os

# 文件路径
CHAT_HISTORY_FILE = "chat_history.json"

# 读取聊天记录
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

# 保存聊天记录
def save_chat_history(chat_history):
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(chat_history, file)

# 删除聊天记录
def delete_chat_history(chat_id):
    chat_history = load_chat_history()
    if chat_id in chat_history:
        del chat_history[chat_id]
        save_chat_history(chat_history)
    # 如果没有剩余聊天记录，清空文件并重置计数器
    if not chat_history:
        os.remove(CHAT_HISTORY_FILE)
        st.session_state.chat_count = 0

# 初始化聊天记录
if 'history' not in st.session_state:
    st.session_state.history = []

# 初始化聊天历史记录计数器
if 'chat_count' not in st.session_state:
    st.session_state.chat_count = len(load_chat_history())

# 欢迎语句
welcome_message = {"role": "bot", "text": "Hi~我是AIstinct，您的专属智能对话助手"}
# 如果聊天历史为空，添加欢迎语句
if not st.session_state.history:
    st.session_state.history.append(welcome_message)

# 在侧边栏顶部左侧添加标题和头像
with st.sidebar:
    st.markdown("""
        <div style="text-align:left;">
            <img src="https://s2.loli.net/2024/06/14/anpbUxW8vz1Vo42.png" class="sidebar-avatar" alt="Bot Avatar">
            <h2 style="color: rgba(0, 0, 0, 0.6); margin-bottom: 20px; font-size: 36px;">AIstinct</h2>
        </div>
    """, unsafe_allow_html=True)

     # 新建聊天按钮
    if st.button("新建聊天"):
        st.session_state.chat_count += 1
        new_chat_id = f"chathistory{st.session_state.chat_count}"
        chat_history = load_chat_history()
        chat_history[new_chat_id] = []  # 创建一个新的空聊天记录
        save_chat_history(chat_history)
        st.session_state.history = []  # 重置当前聊天界面为初始状态

    st.markdown("---")
    
    # 添加折叠按钮
    with st.expander("参数控制"):
        st.write("在这里调整生成参数")
        max_length = st.slider("max_length", 0, 32768, 8192)
        top_p = st.slider("top_p", 0.0, 1.0, 0.8)
        temperature = st.slider("temperature", 0.0, 1.0, 0.69)

    # 读取历史聊天记录
    st.markdown("### 查看聊天历史")
    chat_history = load_chat_history()
    for chat_id in chat_history.keys():
        cols = st.columns([4, 1])
        with cols[0]:
            if st.button(chat_id):
                st.session_state.history = chat_history[chat_id]
        with cols[1]:
            if st.button("🗑️", key=f"delete_{chat_id}"):
                delete_chat_history(chat_id)
                st.experimental_rerun()  # 刷新页面以更新聊天记录列表

# 添加自定义样式
st.markdown("""
    <style>
        .input-container {
            display: flex;
            align-items: center;
            border: 1px solid #ddd;
            border-radius: 20px;
            padding: 10px;
            width: 60%;
            margin: 0 auto;
            background-color: #fff;
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
        }
        .input-box {
            flex: 1;
            border: none;
            outline: none;
            padding: 10px;
            padding-left: 30px;
            font-size: 16px;
            border-radius: 20px;
            margin-right: 10px;
            color: #333;
            background-color: #f7f7f7;
        }
        .upload-button {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            cursor: pointer;
        }
        .upload-button img {
            width: 20px;
            height: 20px;
        }
        .input-box::placeholder {
            color: #888;
            opacity: 1;
        }
        .send-button {
            background: url('https://s2.loli.net/2024/06/14/pDBnfJh4T6AE5jm.png') no-repeat center center;
            background-size: contain;
            width: 30px;
            height: 30px;
            border: none;
            cursor: pointer;
            background-color: transparent;
        }
        .chat-container {
            height: 10vh;  /* 设置对话区域高度为视窗高度的80% */
            overflow-y: auto;  /* 允许垂直滚动 */
            margin: 0 auto;  /* 水平居中 */
            padding: 0;  /* 去除内边距 */
            border: none;  /* 移除边框 */
            border-radius: 0;  /* 去除圆角 */
            width: 100%;  /* 调整宽度为页面宽度的95% */
            box-shadow: none;  /* 去除阴影效果 */
            display: flex;
            flex-direction: column;
        }
        .bubble {
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            max-width: 70%;
            word-wrap: break-word;
            display: inline-block;
        }
        .user-bubble {
            background-color: #cfe9ff;
            align-self: flex-end;
            float: right;
            clear: both;
        }
        .bot-bubble {
            background-color: #f1f1f1;
            align-self: flex-start;
            float: left;
            clear: both;
        }
        .clearfix::after {
            content: "";
            clear: both;
            display: table;
        }
        .bot-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .sidebar-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
        }
        .message-container {
            display: flex;
            align-items: center;
        }
        .bot-message {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 显示对话内容
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.history:
    if message["role"] == "user":
        st.markdown(f'<div class="bubble user-bubble clearfix">{message["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div class="bot-message">
                <img src="https://s2.loli.net/2024/06/14/anpbUxW8vz1Vo42.png" class="bot-avatar" alt="Bot Avatar">
                <div class="bubble bot-bubble clearfix">{message["text"]}</div>
            </div>
        ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 用户输入框和发送按钮
st.markdown("""
    <div class="input-container">
        <input type="text" id="user_input" class="input-box" placeholder="请输入您的需求">
        <button id="send_button" class="send-button"></button>
        <label for="file-upload" class="upload-button">
            <img src="https://s2.loli.net/2024/06/14/zdrxQl2IXGvEZO5.png" alt="Upload">
        </label>
        <input type="file" id="file-upload" style="display: none;">
    </div>
""", unsafe_allow_html=True)

# JavaScript 处理提交
st.markdown("""
    <script>
        document.getElementById("send_button").addEventListener("click", function() {
            var userInput = document.getElementById("user_input").value;
            if (userInput) {
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "/", true);
                xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        window.location.reload(); // Refresh page to reflect new chat history
                    }
                };
                xhr.send("user_input=" + encodeURIComponent(userInput));
            }
        });
    </script>
""", unsafe_allow_html=True)

# 处理用户输入
query_params = st.query_params
if "user_input" in query_params:
    user_input = query_params["user_input"]
    if user_input:
        # 更新历史记录
        st.session_state.history.append({"role": "user", "text": user_input})

        # 模拟发送请求到大模型，需替换为实际模型服务的API
        response = requests.post(
            "http://your-model-server-endpoint",  # 替换为你的模型服务器地址
            json={"input": user_input, "max_length": max_length, "top_p": top_p, "temperature": temperature}
        )

        # 解析响应
        if response.status_code == 200:
            model_reply = response.json().get("reply", "无响应")
            st.session_state.history.append({"role": "bot", "text": model_reply})
        else:
            st.session_state.history.append({"role": "bot", "text": "模型服务器未响应"})
        
    # 保存当前聊天记录
    chat_history[f"chathistory{st.session_state.chat_count}"] = st.session_state.history
    save_chat_history(chat_history)

# 清理历史记录按钮
if st.sidebar.button("清理会话历史"):
    st.session_state.history = []

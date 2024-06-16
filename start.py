import streamlit as st
from login import login

# 设置页面配置
st.set_page_config(page_title="应用程序", page_icon=":rocket:", layout="centered")

# 自定义 CSS 样式
custom_css = """
<style>
body {
    background: url('https://example.com/your-background.jpg') no-repeat center center fixed;  /* 背景图片URL */
    background-size: cover;
    margin: 0;  /* 去除默认边距 */
}
.welcome-title {
    font-size: 48px;  /* 调整字体大小 */
    color: black;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0);
    text-align: center;
    position: relative;
    top: 20vh;  /* 设置距离页面顶部的高度 */
    margin-left: 15px;  /* 去除默认外边距 */
}
.blank {
    font-size: 144px;
}
.welcome-subtitle {
    font-size: 24px;  /* 调整字体大小 */
    color: black;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0);
    text-align: center;
    position: relative;
    top: 22vh;  /* 设置距离页面顶部的高度 */
    margin-left: -10px;  /* 去除默认外边距 */
}
.start-button {
    display: flex;
    justify-content: center;
    position: relative;
    top: 15vh;  /* 设置距离页面顶部的高度 */
}
.start-button .stButton>button {
    font-size: 20px;
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    border: none;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
    cursor: pointer;
    text-decoration: none;
}
.start-button .stButton>button:hover {
    background-color: #45a049;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 定义一个函数来处理按钮点击事件
def on_button_click():
    st.session_state.page = 'Login'
    st.experimental_rerun()

# 开始界面函数
def start_page():
    st.markdown("<h1 class='welcome-title'>AIstinct</h1>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-subtitle'>Wanna explore more? Click and start!</p>", unsafe_allow_html=True)
    st.markdown("<div class='start-button'>", unsafe_allow_html=True)
    st.markdown("<h1 class='blank'> </h1>", unsafe_allow_html=True)
    # 使用列布局来调整按钮位置
    col1, col2, col3,col4,col5,col6,col7 = st.columns(7)
    with col4:
        if st.button("START", key="start_button"):
            st.session_state.page = 'Login'
            st.experimental_rerun()

# 页面导航逻辑
if 'page' not in st.session_state:
    st.session_state.page = 'Start'

if st.session_state.page == 'Start':
    start_page()
elif st.session_state.page == 'Login':
    login()

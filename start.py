import streamlit as st
import base64
from login import login

# 设置页面配置
st.set_page_config(page_title="AIstinct", page_icon=":rocket:", layout="centered")

# 定义函数以设置背景图片
def main_bg(main_bg):
    main_bg_ext = main_bg.split('.')[-1]  # 获取文件扩展名
    with open(main_bg, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{main_bg_ext};base64,{image_base64}) no-repeat center center;
            background-size: contain;  /* 背景图片保持比例自适应调整 */
            background-position: center;  /* 图片居中显示 */
            background-color: white;  /* 设置背景颜色 */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
# 示例：设置背景图片（替换为你的图片文件路径）
  # 替换为你自己的图片路径

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
    font-weight: 500; /*调整字体粗细 */
    margin-left: 73px;  /* 去除默认外边距 */
}
.header{
    font-size: 36px;
    margin-left: 285px;
}
.subheader1{
    font-size: 22px;
    margin-left: 83px;
}
.subheader2{
    font-size: 22px;
    margin-left: 80px;
}
.blank {
    font-size: 96px;
    color: black;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0);
    text-align: center;
    position: relative;
    top: 22vh;  /* 设置距离页面顶部的高度 */
    margin-left: -10px;  /* 去除默认外边距 */
}
.welcome-subtitle {
    font-size: 48px;  /* 调整字体大小 */
    font-weight: 600; /*调整字体粗细 */
    margin-left: 150px;  /* 去除默认外边距 */
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
    st.markdown("<h1 class='blank'> </h1>", unsafe_allow_html=True)
    st.markdown("<h1 class='header'>AIstinct</h1>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-title'>Design spaces. Get creative.</p>", unsafe_allow_html=True)
    st.markdown("<p class='welcome-subtitle'>Elevate your living.</p>", unsafe_allow_html=True)
    st.markdown("<p class='subheader1'>Easy to explore. Friendly to use. Just ask and AIstinct can</p>", unsafe_allow_html=True)
    st.markdown("<p class='subheader2'>assist with interior design, Q&A, brainstroming, and more.</p>", unsafe_allow_html=True)
    st.markdown("<div class='start-button'>", unsafe_allow_html=True)

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
else:
    login()

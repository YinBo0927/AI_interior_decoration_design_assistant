import streamlit as st
import replicate
import os
import dashscope
from http import HTTPStatus
from dashscope import Generation
from sd.page import sd_module
from PIL import Image
import unicodedata
import base64
import cv2
from img2video import img2video

# 显示图片
def render_img_html(image_b64):
    st.markdown(f"<img style='width: 500px;height: 500px;' src='data:image/png;base64, {image_b64}'/>", unsafe_allow_html=True)

def image_to_base64(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    _, encoded_image = cv2.imencode(".png", image)
    base64_image = base64.b64encode(encoded_image.tobytes()).decode("utf-8")
    return base64_image

# 判断是否有中文
def contains_chinese(s):
    for c in s:
        if 'CJK UNIFIED' in unicodedata.name(c):
            return True
    return False

def main():
    # App title
    st.title("🤖💬 AIstinct")
    st.caption("an AI assistant who can help you in interior decoration design")
    
    # st.subheader('an AI interior decoration design assistant')

    # Replicate Credentials
    with st.sidebar:
        st.markdown("""
        <div style="margin-top: 40px; display: flex; align-items: center;">
            <div>
                <img src="https://s2.loli.net/2024/06/14/anpbUxW8vz1Vo42.png" class="sidebar-avatar" alt="Bot Avatar" style="width: 50px; height: 50px; margin-right: 10px;">
            </div>
            <div>
                <h1 style="margin: 0;">AIstinct</h1>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
        # 添加自定义样式
        st.markdown("""
            <style>
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
            </style>
        """, unsafe_allow_html=True)
        st.divider()
        model = st.selectbox(label="Please select the model", options=("AIstinct_img", "AIstinct_video"))
        upload_image = st.file_uploader("Upload Image Here", accept_multiple_files=False, type = ['jpg', 'png'])
        if upload_image:
            st.success("load image success")
            #st.image(upload_image, width=200) #持保留意见看看要不要



    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    message_history_list=[]

    # Display or clear chat messages
    #print(len(st.session_state.messages))
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if os.path.isfile(message["content"]):
                #st.image(message["content"],width=400)
                render_img_html(image_to_base64(message["content"]))
            else:
                st.write(message["content"])

    def clear_chat_history(message_history_list):
        #st.session_state.messages.clear()
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
        message_history_list=[]
        
    st.sidebar.button('🗑️ Clear Chat History', on_click=clear_chat_history(message_history_list))
    st.sidebar.divider()
    st.sidebar.markdown(" **If you have any problem, feel free to contact us:**")
    st.sidebar.markdown(":email: E-mail: yb0927@outlook.com"  )
    st.sidebar.markdown(":iphone: Phone: 19303019326")
    st.sidebar.markdown(":balloon: [github source](https://github.com/YinBo0927/AI_interior_decoration_design_assistant)")

    # 这里实现一下两个
    def generate_llm_output(prompt_input, messages):
        dashscope.api_key = "sk-2d05db839dc94bbea634c77e2041ed1c"
        prompt = f'''Your name is AIstinct who is an assistant to help interior decoration design, if the user mentions a decoration request or some modifications of previous decoration requests in the current user_input, you need to simplify and summarize it into a short description suitable for generating an image by ControlNet and Stable Diffusion. The description should be one sentence long. Do not include any extra information or context. Add "需求: " at the beginning of your response. 
                                    Example:
                                        User: I'm looking to get my dining area done up. I want a nice table with some chairs, and it would be great to have a clock right above the table on the wall. I like the artist Fedot Sychkov's style, so something along those lines with soft, muted colors. Also, I've always admired detailed art, but I'm into minimalism too, so maybe an ultra-fine detailed painting that still feels minimalist. Keep it simple but elegant, please.
                                        AIstinct: 需求: a dining room table with chairs and a clock on the wall above it and a clock on the wall, Fedot Sychkov, muted colors, an ultrafine detailed painting, minimalism
                            
                            If the user mentions a decoration request or some modifications of previous decoration requests in the messages but not in current user_input, you need to focus mainly on the current user_input and chat with the user in ordinary ways. Do not do the simplification and summary.
                                    Example:
                                        User: I'm looking to get my dining area done up. I want a nice table with some chairs, and it would be great to have a clock right above the table on the wall. I like the artist Fedot Sychkov's style, so something along those lines with soft, muted colors. Also, I've always admired detailed art, but I'm into minimalism too, so maybe an ultra-fine detailed painting that still feels minimalist. Keep it simple but elegant, please.
                                        That's great. Thank you!
                                        AIstinct: You are welcome! Please let me know if you have any other idea.

                            If the user do not mention a decoration request in current user_input and messages, chat with the user in ordinary ways      
                '''
        if len(messages) == 0:
            messages = [{'role': 'user', 'content': prompt}]
            include_history = False
            
        if "I" in prompt_input.upper() or "who" in prompt_input.lower() or "hello" in prompt_input.lower():
            include_history = True
        else:
            include_history = False
        
        messages.append({'role': 'user', 'content': prompt_input})
        
        messages_to_send = messages if include_history else [{'role': 'user', 'content': prompt_input}]
        
        response = Generation.call(model="qwen-max",
                                    messages=messages_to_send,
                                    result_format='message',  
                                    stream=False, 
                                    incremental_output=False 
                                    )
        
        if response.status_code == HTTPStatus.OK:
            assistant_reply = response['output']['choices'][0]['message']['content']
        else:
            print(f"Error: Request id: {response.request_id}, Status code: {response.status_code}, Error message: {response.message}")
            
        return assistant_reply


    if model == "AIstinct_img":
        if upload_image:
            if prompt := st.chat_input(placeholder="Ask me anything!(Only Support Engilsh Now)"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)
            if st.session_state.messages[-1]["role"] != "assistant":
                if contains_chinese(prompt):
                    st.error("Sorry, we only support English now.")
                else:
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            response = generate_llm_output(prompt,message_history_list)
                            if "需求" in response:
                                #print(response)
                                placeholder = st.empty()
                                full_response = 'Here is the decoration design followed your request.'
                                placeholder.markdown(full_response)
                                output = sd_module.use_sd_api(response[3:],upload_image)
                                #st.image(output,width=400)
                                render_img_html(image_to_base64(output))
                                #st.video(img2video(output),format='video/mp4')
                                response = output
                            else:
                                placeholder = st.empty()
                                full_response = ''
                                for item in response:
                                    full_response += item
                                    placeholder.markdown(full_response)
                                placeholder.markdown(full_response)
                    message = {"role": "assistant", "content": response} #这里不确定有没有问题
                    st.session_state.messages.append(message)
                            
                
        else:
            if prompt := st.chat_input(placeholder="Ask me anything!(Only Support Engilsh Now)"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)
            if st.session_state.messages[-1]["role"] != "assistant":
                if contains_chinese(prompt):
                        st.error("Sorry, we only support English now.")
                else:
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            response = generate_llm_output(prompt,message_history_list)
                            if "需求" in response:
                                # placeholder = st.empty()
                                # full_response = 'Please upload your rough room image first and I will design it for you'
                                # placeholder.markdown(full_response)
                                # print(response)
                                placeholder = st.empty()
                                full_response = 'Here is the decoration design followed your request.'
                                placeholder.markdown(full_response)
                                output = sd_module.use_sd_api(response[3:],upload_image)
                                #st.image(output,width=400)
                                render_img_html(image_to_base64(output))
                                # 展示视频
                                #st.video(img2video(output),format='video/mp4',autoplay=True)
                                response = output
                            else:
                                placeholder = st.empty()
                                full_response = ''
                                for item in response:
                                    full_response += item
                                    placeholder.markdown(full_response)
                                placeholder.markdown(full_response)
                    message = {"role": "assistant", "content": response}
                    st.session_state.messages.append(message)
    elif model == "AIstinct_video":
        if upload_image:
            if prompt := st.chat_input(placeholder="Ask me anything!(Only Support Engilsh Now)"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)
            if st.session_state.messages[-1]["role"] != "assistant":
                if contains_chinese(prompt):
                    st.error("Sorry, we only support English now.")
                else:
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            response = generate_llm_output(prompt,message_history_list)
                            if "需求" in response:
                                print(response)
                                placeholder = st.empty()
                                full_response = 'Here is the decoration design followed your request.'
                                placeholder.markdown(full_response)
                                output = sd_module.use_sd_api(response[3:],upload_image)
                                #st.image(output,width=400)
                                #render_img_html(image_to_base64(output))
                                output= img2video(output)
                                st.video(output,format='video/mp4')
                                response = output
                            else:
                                placeholder = st.empty()
                                full_response = ''
                                for item in response:
                                    full_response += item
                                    placeholder.markdown(full_response)
                                placeholder.markdown(full_response)
                    message = {"role": "assistant", "content": response} #这里不确定有没有问题
                    st.session_state.messages.append(message)
                            
                
        else:
            if prompt := st.chat_input(placeholder="Ask me anything!(Only Support Engilsh Now)"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)
            if st.session_state.messages[-1]["role"] != "assistant":
                if contains_chinese(prompt):
                        st.error("Sorry, we only support English now.")
                else:
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            response = generate_llm_output(prompt,message_history_list)
                            if "需求" in response:
                                # placeholder = st.empty()
                                # full_response = 'Please upload your rough room image first and I will design it for you'
                                # placeholder.markdown(full_response)
                                # print(response)
                                placeholder = st.empty()
                                full_response = 'Here is the decoration design followed your request.'
                                placeholder.markdown(full_response)
                                output = sd_module.use_sd_api(response[3:],upload_image)
                                #st.image(output,width=400)
                                #render_img_html(image_to_base64(output))
                                # 展示视频
                                output = img2video(output)
                                st.video(output,format='video/mp4',autoplay=True)
                                response = output
                            else:
                                placeholder = st.empty()
                                full_response = ''
                                for item in response:
                                    full_response += item
                                    placeholder.markdown(full_response)
                                placeholder.markdown(full_response)
                    message = {"role": "assistant", "content": response}
                    st.session_state.messages.append(message)
            

if __name__ == '__main__':
    main()
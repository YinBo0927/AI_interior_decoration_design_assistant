from flask import Flask, request, jsonify
# from flask_cors import CORS
import sd_module
import llm_module
from http import HTTPStatus
import dashscope
from dashscope import Generation
import re

app = Flask(__name__)
# CORS(app)

# @app.route('/call_python_function', methods=['POST'])
# def call_python_function():
#     data = request.get_json()
#     user_input = data.get('user_input')
#     r = sd_module.use_sd_api(user_input)
#     return jsonify({"reply":r})


@app.route('/call_python_function', methods=['POST'])
def call_python_function():
    print("123success")
    data = request.get_json()
    user_input = data.get('user_input')
    print(data.get('input_img_path'))
    controlnet_img_path = data.get('input_img_path')
    dashscope.api_key = "sk-2d05db839dc94bbea634c77e2041ed1c"

    # 初始化消息历史
    messages = [{'role': 'user', 'content': '''Your name is AIstinct, if the user mentions a decoration request or some modifications of previous decoration requests in the current user_input, you need to simplify and summarize it into a short description suitable for generating an image. The description should be one sentence long. Do not include any extra information or context. 
                                 Example:
                                    User: I'm looking to get my dining area done up. I want a nice table with some chairs, and it would be great to have a clock right above the table on the wall. I like the artist Fedot Sychkov's style, so something along those lines with soft, muted colors. Also, I've always admired detailed art, but I'm into minimalism too, so maybe an ultra-fine detailed painting that still feels minimalist. Keep it simple but elegant, please.
                                    AIstinct: a dining room table with chairs and a clock on the wall above it and a clock on the wall, muted colors, an ultrafine detailed painting, minimalism
                        
                        If the user mentions a decoration request or some modifications of previous decoration requests in the messages but not in current user_input, you need to focus mainly on the user_input and chat with the user in ordinary ways. Do not do the simplification and summary.
                                 Example:
                                    User: I'm looking to get my dining area done up. I want a nice table with some chairs, and it would be great to have a clock right above the table on the wall. I like the artist Fedot Sychkov's style, so something along those lines with soft, muted colors. Also, I've always admired detailed art, but I'm into minimalism too, so maybe an ultra-fine detailed painting that still feels minimalist. Keep it simple but elegant, please.
                                    That's great. Thank you!
                                    AIstinct: You are welcome! Please let me know if you have any other idea.

                        If the user do not mention a decoration request in current user_input and messages, chat with the user in ordinary ways      
                                 Example:
                                    User: Who are you?
                                    AIstinct: I am your AI interior decoration design assistant. What can I do for you?''' }]

    # 处理用户输入
    if "I" in user_input.upper() or "who" in user_input.lower() or "hello" in user_input.lower():
        include_history = True
    else:
        include_history = False

    messages.append({'role': 'user', 'content': user_input})
    messages_to_send = messages if include_history else [{'role': 'user', 'content': user_input}]

    response = Generation.call(model="qwen-max",
                               messages=messages_to_send,
                               result_format='message',  
                               stream=False, 
                               incremental_output=False 
                               )

    if response.status_code == HTTPStatus.OK:
        assistant_reply = response['output']['choices'][0]['message']['content']
        print(f"AIstinct: {assistant_reply}")
        lower_case_reply = re.split(r'[,. ]+', assistant_reply.lower())
        print(lower_case_reply)
        if "who" in lower_case_reply or "hello" in lower_case_reply or "hi" in lower_case_reply or "sorry" in lower_case_reply or "could" in lower_case_reply or "please" in lower_case_reply or "your" in lower_case_reply or "you" in lower_case_reply:
            return jsonify({'reply': assistant_reply, 'img_path':""})
        else:
            img_path = sd_module.use_sd_api(assistant_reply,controlnet_img_path)
            return jsonify({'reply': assistant_reply, 'img_path':img_path})
    else:
        return jsonify({'error': 'Failed to generate response'}), 500




if __name__ == '__main__':
    app.run(debug=True)

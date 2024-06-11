import dashscope
from http import HTTPStatus
from dashscope import Generation

def multi_round():
    dashscope.api_key = "sk-2d05db839dc94bbea634c77e2041ed1c"
    prompt = f'''Your name is AIstinct, if the user mentions a decoration request or some modifications of previous decoration requests in the current user_input, you need to simplify and summarize it into a short description suitable for generating an image. The description should be one sentence long. Do not include any extra information or context. 
                                 Example:
                                    User: I'm looking to get my dining area done up. I want a nice table with some chairs, and it would be great to have a clock right above the table on the wall. I like the artist Fedot Sychkov's style, so something along those lines with soft, muted colors. Also, I've always admired detailed art, but I'm into minimalism too, so maybe an ultra-fine detailed painting that still feels minimalist. Keep it simple but elegant, please.
                                    AIstinct: a dining room table with chairs and a clock on the wall above it and a clock on the wall, Fedot Sychkov, muted colors, an ultrafine detailed painting, minimalism
                        
                        If the user mentions a decoration request or some modifications of previous decoration requests in the messages but not in current user_input, you need to focus mainly on the user_input and chat with the user in ordinary ways. Do not do the simplification and summary.
                                 Example:
                                    User: I'm looking to get my dining area done up. I want a nice table with some chairs, and it would be great to have a clock right above the table on the wall. I like the artist Fedot Sychkov's style, so something along those lines with soft, muted colors. Also, I've always admired detailed art, but I'm into minimalism too, so maybe an ultra-fine detailed painting that still feels minimalist. Keep it simple but elegant, please.
                                    That's great. Thank you!
                                    AIstinct: You are welcome! Please let me know if you have any other idea.

                        If the user do not mention a decoration request in current user_input and messages, chat with the user in ordinary ways      
                                 Example:
                                    User: Who are you?
                                    AIstinct: I am your AI interior decoration design assistant. What can I do for you?
              '''
    
    # Initially send the prompt to the model
    messages = [{'role': 'user', 'content': prompt}]

    # 初始化状态变量，只有当需要历史信息时才设置为True
    include_history = False

    while True:
        user_input = input("User Input: ")
        if user_input.lower() == "exit":
            break
        
        # 根据用户输入更新状态变量
        if "I" in user_input.upper() or "who" in user_input.lower() or "hello" in user_input.lower():
           include_history = True
        else:
            include_history = False
        #include_history = 'I' in user_input

        # 将当前用户输入添加到消息历史中
        messages.append({'role': 'user', 'content': user_input})
        
        # 如果需要历史信息，传递所有消息，否则只传递最新消息
        messages_to_send = messages if include_history else [{'role': 'user', 'content': user_input}]

        # 调用生成模型
        response = Generation.call(model="qwen-turbo",
                                   messages=messages_to_send,
                                   result_format='message',  
                                   stream=False, 
                                   incremental_output=False 
                                   )
        
        # 检查响应并打印助手的回复
        if response.status_code == HTTPStatus.OK:
            assistant_reply = response['output']['choices'][0]['message']['content']
            print(f"Assistant: {assistant_reply}")
        else:
            print(f"Error: Request id: {response.request_id}, Status code: {response.status_code}, Error message: {response.message}")

if __name__ == '__main__':
    multi_round()

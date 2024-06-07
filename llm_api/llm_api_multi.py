from http import HTTPStatus
from dashscope import Generation
import dashscope
dashscope.api_key="sk-2d05db839dc94bbea634c77e2041ed1c"

def multi_round(user_input):
    prompt = f'''Your name was AIstinct, When the user mentions a renovation request, you need to simplify and summarize it into a short description suitable for generating an image. The description should be one sentence long. Do not include any extra information or context.
                                 Examples:

                                    User: Hi, I'm looking to get my dining area done up. I want a nice table with some chairs, and it would be great to have a clock right above the table on the wall. I like the artist Fedot Sychkov's style, so something along those lines with soft, muted colors. Also, I've always admired detailed art, but I'm into minimalism too, so maybe an ultra-fine detailed painting that still feels minimalist. Keep it simple but elegant, please.
                                    AIstinct: a dining room table with chairs and a clock on the wall above it and a clock on the wall, Fedot Sychkov, muted colors, an ultrafine detailed painting, minimalism

                                    User: {user_input}
                                    AIstinct:'''
    messages = [{'role': 'user', 'content': prompt}]
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               # 将输出设置为"message"格式
                               result_format='message')
    if response.status_code == HTTPStatus.OK:
        print(response)
        # 将assistant的回复添加到messages列表中
        messages.append({'role': response.output.choices[0]['message']['role'],
                         'content': response.output.choices[0]['message']['content']})
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        # 如果响应失败，将最后一条user message从messages列表里删除，确保user/assistant消息交替出现
        messages = messages[:-1]
    # 将新一轮的user问题添加到messages列表中
    messages.append({'role': 'user', 'content': '不放糖可以吗？'})
    # 进行第二轮模型的响应
    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               result_format='message',  # 将输出设置为"message"格式
                               )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    multi_round('''I'd like a cozy kitchen with a dining area, maybe a small table and chairs. 
    It would be nice to have a vase on the counter by the window to add some life. The lighting should be soft, 
    like what you'd find in a Claire Dalby design. 
    Essentially, I'm looking for something light and airy, with a spacious feel.''')
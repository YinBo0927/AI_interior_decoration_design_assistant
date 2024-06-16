import base64
import requests
import json

def img2video(img_path):
    # 读取图片并转换为base64编码字符串
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # 构建请求数据
    data = {
        "image": encoded_string
    }

    # 发送POST请求到Flask服务器
    response = requests.post('https://u245871-8b28-876cfcef.westc.gpuhub.com:8443/process_image', headers={'Content-Type': 'application/json'}, json=data)

    # 保存返回的mp4文件
    if response.status_code == 200:
        with open("output_video.mp4", "wb") as video_file:
            video_file.write(response.content)
        print("Video saved as output_video.mp4")
        return "output_video.mp4"
    else:
        print("Error:", response.json())

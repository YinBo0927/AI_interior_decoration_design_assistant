from flask import Flask, request, jsonify, send_file
import base64
import subprocess
import os
import sys

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.json
    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400
    
    image_base64 = data['image']
    
    # 将base64字符串解码并保存为图片文件
    image_data = base64.b64decode(image_base64)
    image_folder = 'image'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    
    image_path = os.path.join(image_folder, 'input_image.png')
    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)
    
    # 调用外部程序并实时打印输出
    try:
        process = subprocess.Popen(['python3', 'main.py', '--config', 'argument.yml'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 实时打印 stdout 和 stderr
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                sys.stdout.flush()
        
        stderr = process.stderr.read()
        if process.returncode != 0:
            return jsonify({'error': 'Error running main.py', 'details': stderr}), 500
        
    except Exception as e:
        return jsonify({'error': 'Exception running main.py', 'details': str(e)}), 500
    
    # 获取处理后的视频文件
    video_folder = 'video'
    video_path = os.path.join(video_folder, 'input_image_swing.mp4')
    if not os.path.exists(video_path):
        return jsonify({'error': 'Processed video not found'}), 500
    
    # 清理image文件夹中的图片
    try:
        for filename in os.listdir(image_folder):
            file_path = os.path.join(image_folder, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    except Exception as e:
        return jsonify({'error': 'Failed to clean up images', 'details': str(e)}), 500

    # 发送视频文件作为响应
    return send_file(video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(port=6006)

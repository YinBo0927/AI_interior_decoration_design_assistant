from flask import Flask, request, jsonify
import module

app = Flask(__name__)

@app.route('/call_python_function', methods=['POST'])
def call_python_function():
    r = module.use_api()
    return jsonify({"result":r})


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import webview
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    phone = data.get('phone')
    code = data.get('code')
    
    # 这里添加验证逻辑
    if phone and code:
        return jsonify({'status': 'success', 'message': '登录成功'})
    return jsonify({'status': 'error', 'message': '登录失败'})

def create_app():
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
    return app

if __name__ == '__main__':
    app = create_app()
    # 创建窗口
    webview.create_window('登录', app, width=400, height=600)
    webview.start() 
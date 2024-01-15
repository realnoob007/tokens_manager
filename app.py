from flask import Flask, Response, jsonify, render_template, request, redirect, url_for, session
from flask_cors import CORS
import token_manager_db
import os
import update_config

app = Flask(__name__)
cors = CORS(app)
app.secret_key = 'aldjowiqodjoapdpapdjpadpawdwad'  # Replace with a strong secret key

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, 'usertokens.txt')
CONFIG_DIR = '/code/manager'

# Define the admin username and password
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "gomakemoney"

# 定义API密钥
API_KEY = "gomakemoney"

# 在app.py中添加验证函数
def validate_api_key():
    if request.headers.get('API-Key') != API_KEY:
        return Response("Unauthorized", status=401)


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file:
            add_tokens_from_file(file)
    tokens = token_manager_db.get_tokens_details()
    return render_template('index.html', tokens=tokens)

def add_tokens_from_file(file):
    new_tokens = [line.strip() for line in file.readlines() if line.strip()]
    for token in new_tokens:
        token_manager_db.add_token(token, 30)
        update_config.add_token_to_config(token)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Debug statements
        print(f"Received username: {username}")
        print(f"Received password: {password}")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add():
    token = request.form['token']
    validity_days_str = request.form.get('validity_days', '30')
    validity_days = int(validity_days_str) if validity_days_str.isdigit() else 30
    try:
        token_manager_db.add_token(token, validity_days)
        update_config.update_token_in_all_configs(CONFIG_DIR, token, 'add')
    except Exception as e:
        print(f"Error adding token: {e}")
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    token = request.form['token']
    try:
        token_manager_db.delete_token(token)
        update_config.update_token_in_all_configs(CONFIG_DIR, token, 'delete')
    except Exception as e:
        print(f"Error deleting token: {e}")
    return redirect(url_for('index'))

@app.route('/api/tokens', methods=['GET'])
def get_all_tokens():
    auth = validate_api_key()
    if auth:
        return auth
    return jsonify(token_manager_db.get_tokens_details())

@app.route('/api/token/<token_id>', methods=['GET'])
def get_token(token_id):
    auth = validate_api_key()
    if auth:
        return auth
    token_info = token_manager_db.get_token_detail(token_id)
    if token_info:
        return jsonify(token_info)
    return Response("Token not found", status=404)

@app.route('/api/token', methods=['POST'])
def api_add_token():
    auth = validate_api_key()
    if auth:
        return auth
    token = request.json.get('token')
    validity_days = request.json.get('validity_days', 30)  # Default to 30 days if not specified
    if token:
        try:
            token_manager_db.add_token(token, validity_days)
            update_config.update_token_in_all_configs(CONFIG_DIR, token, 'add')
            return Response("Token added", status=201)
        except Exception as e:
            return Response(str(e), status=400)
    return Response("Invalid request", status=400)

@app.route('/api/token', methods=['DELETE'])
def api_delete_token():
    auth = validate_api_key()
    if auth:
        return auth
    token = request.json.get('token')
    if token:
        try:
            token_manager_db.delete_token(token)
            update_config.update_token_in_all_configs(CONFIG_DIR, token, 'delete')
            return Response("Token deleted", status=200)
        except Exception as e:
            return Response(str(e), status=400)
    return Response("Invalid request", status=400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

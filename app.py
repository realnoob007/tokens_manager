from flask import Flask, render_template, request, redirect, url_for, session
import token_manager
import os

app = Flask(__name__)
app.secret_key = 'aldjowiqodjoapdpapdjpadpawdwad'  # Replace with a strong secret key

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, 'usertokens.txt')

# Define the admin username and password
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "gomakemoney"


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
    tokens = token_manager.get_tokens_details(TOKEN_FILE)
    return render_template('index.html', tokens=tokens)

def add_tokens_from_file(file):
    new_tokens = [line.strip() for line in file.readlines() if line.strip()]
    for token in new_tokens:
        token_manager.add_token(token.decode('utf-8'), TOKEN_FILE)

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
    try:
        token_manager.add_token(token, TOKEN_FILE)
    except Exception as e:
        print(f"Error adding token: {e}")
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    token = request.form['token']
    try:
        token_manager.delete_token(token, TOKEN_FILE)
    except Exception as e:
        print(f"Error deleting token: {e}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
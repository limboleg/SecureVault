from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from utils import encrypt_data, decrypt_data, generate_key
from cryptography.fernet import InvalidToken

app = Flask(__name__)
app.secret_key = 'supersecretflaskkey'  # Change this in real usage

VAULT_FILE = 'vault.json'
MASTER_PASSWORD = 'admin123'  # For demo. In real usage, hash + secure this.

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered = request.form.get('password')
        if entered == MASTER_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Incorrect master password')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, 'rb') as f:
            encrypted = f.read()
        try:
            data = decrypt_data(encrypted)
            creds = json.loads(data)
        except InvalidToken:
            creds = []
    else:
        creds = []
    return render_template('dashboard.html', creds=creds)

@app.route('/add', methods=['POST'])
def add():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    site = request.form['site']
    username = request.form['username']
    password = request.form['password']

    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, 'rb') as f:
            data = decrypt_data(f.read())
            creds = json.loads(data)
    else:
        creds = []

    creds.append({"site": site, "username": username, "password": password})
    encrypted = encrypt_data(json.dumps(creds))
    with open(VAULT_FILE, 'wb') as f:
        f.write(encrypted)

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

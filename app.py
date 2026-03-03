import json
import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secure_key_2m1_exclusive' # لا تغير هذا السطر

# الملفات
EXERCISES_FILE = 'exercises.json'
USERS_FILE = 'users.json'
CLASS_NAME = "2م1"
ADMIN_NAME = "عبد الحق"
ADMIN_PASSWORD = "123" # غير كلمة السر هنا

# وظائف JSON
def load_json(filename):
    if not os.path.exists(filename): return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return []

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    exercises = load_json(EXERCISES_FILE)
    users_data = load_json(USERS_FILE)
    all_users = [u['username'] for u in users_data]
    subjects = ["الرياضيات", "اللغة العربية", "اللغة الفرنسية", "اللغة الإنجليزية", "التاريخ والجغرافيا", "التربية المدنية", "التربية الإسلامية", "العلوم الطبيعية", "الفيزياء"]
    return render_template('index.html', subjects=subjects, exercises=exercises, current_user=session['username'], admin_name=ADMIN_NAME, users_list=all_users, class_name=CLASS_NAME)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_NAME and password == ADMIN_PASSWORD:
            session['username'] = ADMIN_NAME
            return redirect(url_for('index'))
        users = load_json(USERS_FILE)
        user = next((u for u in users if u['username'] == username), None)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        return "خطأ في البيانات!"
    return render_template('login.html', class_name=CLASS_NAME)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_NAME: return "اسم محجوز!"
        users = load_json(USERS_FILE)
        if any(u['username'] == username for u in users): return "موجود مسبقاً!"
        users.append({"username": username, "password": generate_password_hash(password)})
        save_json(USERS_FILE, users)
        return redirect(url_for('login'))
    return render_template('register.html', class_name=CLASS_NAME)

@app.route('/add_exercise', methods=['POST'])
def add_exercise():
    if 'username' in session:
        all_ex = load_json(EXERCISES_FILE)
        all_ex.insert(0, {"subject": request.form.get('subject'), "content": request.form.get('content'), "author": session['username']})
        save_json(EXERCISES_FILE, all_ex)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_exercise(index):
    if session.get('username') == ADMIN_NAME:
        all_ex = load_json(EXERCISES_FILE)
        if 0 <= index < len(all_ex):
            all_ex.pop(index)
            save_json(EXERCISES_FILE, all_ex)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
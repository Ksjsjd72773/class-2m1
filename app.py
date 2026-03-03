import json
import os
from flask import Flask, render_template, request, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = "simple_class_secret"

EXERCISES_FILE = "exercises.json"
CLASS_NAME = "2م1"
ADMIN_NAME = "عبد الحق"

# إنشاء ملف التمارين
if not os.path.exists(EXERCISES_FILE):
    with open(EXERCISES_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_exercises():
    with open(EXERCISES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_exercises(data):
    with open(EXERCISES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تسجيل دخول بالاسم فقط
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username

        if username == ADMIN_NAME:
            return redirect("/admin")
        return redirect("/class")

    return render_template("login.html", class_name=CLASS_NAME)

# صفحة الطلاب
@app.route("/class")
def class_page():
    if "username" not in session:
        return redirect("/")

    exercises = load_exercises()

    subjects = ["الرياضيات", "اللغة العربية", "اللغة الفرنسية",
                "اللغة الإنجليزية", "العلوم", "الفيزياء","التاريخ و الجغرافيا","مدنية","اسلامية"]

    return render_template(
        "index.html",
        exercises=exercises,
        subjects=subjects,
        current_user=session["username"],
        class_name=CLASS_NAME
    )

# صفحة الأدمن
@app.route("/admin")
def admin_page():
    if session.get("username") != ADMIN_NAME:
        return redirect("/")

    exercises = load_exercises()

    subjects = ["الرياضيات", "اللغة العربية", "اللغة الفرنسية",
                "اللغة الإنجليزية", "العلوم", "الفيزياء"]

    return render_template(
        "admin.html",
        exercises=exercises,
        subjects=subjects,
        current_user=ADMIN_NAME,
        class_name=CLASS_NAME
    )

# إضافة تمرين
@app.route("/add", methods=["POST"])
def add_exercise():
    if "username" not in session:
        return jsonify({"status": "error"})

    all_ex = load_exercises()

    new_ex = {
        "subject": request.form.get("subject"),
        "content": request.form.get("content"),
        "author": session["username"]
    }

    all_ex.insert(0, new_ex)
    save_exercises(all_ex)

    return jsonify({"status": "success", "exercise": new_ex})

# حذف (أدمن فقط)
@app.route("/delete/<int:index>")
def delete_exercise(index):
    if session.get("username") == ADMIN_NAME:
        all_ex = load_exercises()
        if 0 <= index < len(all_ex):
            all_ex.pop(index)
            save_exercises(all_ex)
            return jsonify({"status": "success"})
    return jsonify({"status": "error"})

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = "secret_memory_key"

# ===== الإعدادات =====
CLASS_NAME = "2م1"
ADMIN_NAME = "عبد الحق"

SUBJECTS = [
    "رياضيات",
    "عربية",
    "فرنسية",
    "انجليزية",
    "تاريخ و جغرافيا",
    "علوم",
    "فيزياء"
]

# ===== تخزين مؤقت =====
exercises = []
logged_users = []

# ==============================
# تسجيل الدخول
# ==============================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()

        if username == "":
            return "اكتب اسمك"

        session["username"] = username

        if username not in logged_users:
            logged_users.append(username)

        if username == ADMIN_NAME:
            return redirect("/admin")

        return redirect("/class")

    return render_template("login.html", class_name=CLASS_NAME)


# ==============================
# صفحة الطلاب
# ==============================
@app.route("/class")
def class_page():
    if "username" not in session:
        return redirect("/")

    return render_template(
        "index.html",
        exercises=exercises,
        subjects=SUBJECTS,   # 🔥 نرسل المواد للصفحة
        current_user=session["username"],
        class_name=CLASS_NAME
    )


# ==============================
# صفحة الأدمن
# ==============================
@app.route("/admin")
def admin_page():
    if session.get("username") != ADMIN_NAME:
        return redirect("/")

    return render_template(
        "admin.html",
        exercises=exercises,
        users=logged_users,
        subjects=SUBJECTS,   # 🔥 أيضاً للأدمن
        class_name=CLASS_NAME
    )


# ==============================
# إضافة تمرين
# ==============================
@app.route("/add", methods=["POST"])
def add_exercise():
    if "username" not in session:
        return jsonify({"status": "error"})

    subject = request.form.get("subject")

    if subject not in SUBJECTS:
        return jsonify({"status": "error"})

    new_ex = {
        "content": request.form.get("content"),
        "author": session["username"],
        "subject": subject
    }

    exercises.insert(0, new_ex)

    return jsonify({"status": "success"})


# ==============================
# حذف تمرين
# ==============================
@app.route("/delete/<int:index>")
def delete_exercise(index):
    if session.get("username") == ADMIN_NAME:
        if 0 <= index < len(exercises):
            exercises.pop(index)
            return jsonify({"status": "success"})
    return jsonify({"status": "error"})


# ==============================
# تسجيل الخروج
# ==============================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ==============================
# تشغيل
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
import os

app = Flask(
    __name__,
    template_folder='../Frontend/templates',
    static_folder='../Frontend/static'
)
app.secret_key = "your-secret-key-change-in-production"

DB_PATH = os.path.join(os.path.dirname(__file__), "attendance.db")


# ======================================================
# DATABASE CONNECTION
# ======================================================
def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ======================================================
# DATABASE INITIALIZATION
# ======================================================
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA foreign_keys=ON;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            section TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            class_id INTEGER,
            FOREIGN KEY (class_id) REFERENCES classes(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS teacher_classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER,
            class_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id),
            FOREIGN KEY (class_id) REFERENCES classes(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            class_id INTEGER,
            student_id INTEGER,
            status TEXT,
            UNIQUE(date, class_id, student_id)
        )
    """)

    # Create admin if not exists
    cur.execute("SELECT id FROM teachers WHERE email=?", ("admin@school.com",))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO teachers (name, email, password_hash) VALUES (?, ?, ?)",
            ("Administrator", "admin@school.com", generate_password_hash("admin123"))
        )

    conn.commit()
    conn.close()


# ======================================================
# AUTH ROUTES
# ======================================================
@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM teachers WHERE email=?", (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            session["is_admin"] = (email == "admin@school.com")

            if session["is_admin"]:
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("teacher_dashboard"))

        flash("Invalid email or password", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ======================================================
# ADMIN DASHBOARD
# ======================================================
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = get_db_connection()

    classes = conn.execute('SELECT * FROM classes').fetchall()
    students = conn.execute('SELECT * FROM students').fetchall()
    teachers = conn.execute(
        'SELECT * FROM teachers WHERE email != ?', ('admin@school.com',)
    ).fetchall()

    today = datetime.now().strftime('%Y-%m-%d')

    # Count for stat card
    today_attendance_count = conn.execute(
        'SELECT COUNT(*) FROM attendance WHERE date = ?',
        (today,)
    ).fetchone()[0]

    # FULL attendance records for today (ADMIN VIEW)
    today_records = conn.execute("""
        SELECT
            s.name AS student_name,
            s.roll_no,
            c.name AS class_name,
            c.section,
            a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        JOIN classes c ON a.class_id = c.id
        WHERE a.date = ?
    """, (today,)).fetchall()

    conn.close()

    return render_template(
        'admin_dashboard.html',
        classes=classes,
        students=students,
        teachers=teachers,
        today_attendance_count=today_attendance_count,
        today_records=today_records,
        current_date=datetime.now().strftime('%B %d, %Y')
    )


@app.route("/admin/attendance_history")
def admin_attendance_history():
    if not session.get("is_admin"):
        return redirect(url_for("login"))

    conn = get_db_connection()

    records = conn.execute("""
        SELECT
            a.date,
            c.name AS class_name,
            c.section,
            s.name AS student_name,
            s.roll_no,
            t.name AS teacher_name,
            a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        JOIN classes c ON a.class_id = c.id
        LEFT JOIN teacher_classes tc ON tc.class_id = c.id
        LEFT JOIN teachers t ON tc.teacher_id = t.id
        ORDER BY a.date DESC
    """).fetchall()

    conn.close()

    return render_template(
        "admin_attendance_records.html",
        records=records
    )


# ======================================================
# ADMIN ACTIONS
# ======================================================
@app.route("/admin/add_class", methods=["POST"])
def add_class():
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO classes (name, section) VALUES (?, ?)",
        (request.form["name"], request.form["section"])
    )
    conn.commit()
    conn.close()
    flash("Class added successfully", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete_class/<int:class_id>")
def delete_class(class_id):
    conn = get_db_connection()
    conn.execute("UPDATE students SET class_id=NULL WHERE class_id=?", (class_id,))
    conn.execute("DELETE FROM teacher_classes WHERE class_id=?", (class_id,))
    conn.execute("DELETE FROM classes WHERE id=?", (class_id,))
    conn.commit()
    conn.close()
    flash("Class deleted", "success")
    return redirect(url_for("admin_dashboard"))

# ======================================================
# 🔥 NEW: DELETE ALL CLASSES + RESET ID
# ======================================================
@app.route("/admin/delete_all_classes")
def delete_all_classes():
    if not session.get("is_admin"):
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute("DELETE FROM classes")
    conn.execute("DELETE FROM sqlite_sequence WHERE name='classes'")

    conn.commit()
    conn.close()

    flash("All classes deleted and ID reset successfully", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/add_student", methods=["POST"])
def add_student():
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO students (name, roll_no, class_id) VALUES (?, ?, ?)",
        (request.form["name"], request.form["roll_no"], request.form["class_id"])
    )
    conn.commit()
    conn.close()
    flash("Student added successfully", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete_student/<int:student_id>")
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM attendance WHERE student_id=?", (student_id,))
    conn.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    flash("Student deleted", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/add_teacher", methods=["POST"])
def add_teacher():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO teachers (name, email, password_hash) VALUES (?, ?, ?)",
        (
            request.form["name"],
            request.form["email"],
            generate_password_hash(request.form["password"])
        )
    )
    teacher_id = cur.lastrowid

    for cid in request.form.getlist("class_ids"):
        conn.execute(
            "INSERT INTO teacher_classes (teacher_id, class_id) VALUES (?, ?)",
            (teacher_id, cid)
        )

    conn.commit()
    conn.close()
    flash("Teacher added successfully", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete_teacher/<int:teacher_id>")
def delete_teacher(teacher_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM teacher_classes WHERE teacher_id=?", (teacher_id,))
    conn.execute("DELETE FROM teachers WHERE id=?", (teacher_id,))
    conn.commit()
    conn.close()
    flash("Teacher deleted", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/assign_teacher_classes/<int:teacher_id>", methods=["POST"])
def assign_teacher_classes(teacher_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM teacher_classes WHERE teacher_id=?", (teacher_id,))
    for cid in request.form.getlist("class_ids"):
        conn.execute(
            "INSERT INTO teacher_classes (teacher_id, class_id) VALUES (?, ?)",
            (teacher_id, cid)
        )
    conn.commit()
    conn.close()
    flash("Teacher classes updated", "success")
    return redirect(url_for("admin_dashboard"))


# ======================================================
# TEACHER DASHBOARD
# ======================================================
@app.route("/teacher/dashboard")
def teacher_dashboard():
    if session.get("is_admin") or not session.get("user_id"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    classes = conn.execute("""
        SELECT c.*
        FROM classes c
        JOIN teacher_classes tc ON c.id = tc.class_id
        WHERE tc.teacher_id = ?
    """, (session["user_id"],)).fetchall()
    conn.close()

    return render_template("teacher_dashboard.html", classes=classes)


# ======================================================
# TAKE ATTENDANCE
# ======================================================
@app.route("/teacher/take_attendance/<int:class_id>", methods=["GET", "POST"])
def take_attendance(class_id):

    # 🔐 AUTH CHECK (keep as it is)
    if session.get("is_admin") or not session.get("user_id"):
        return redirect(url_for("login"))

    # 🔴 ADD FROM HERE (THIS IS THE EXACT PLACE)
    today = datetime.now().strftime("%Y-%m-%d")

    conn = get_db_connection()

    existing = conn.execute(
        "SELECT 1 FROM attendance WHERE date = ? AND class_id = ? LIMIT 1",
        (today, class_id)
    ).fetchone()

    if existing:
        conn.close()
        flash("Attendance for this class has already been taken today.", "warning")
        return redirect(url_for("teacher_attendance_history"))
    # 🔴 ADD TILL HERE

    # ⬇️ EXISTING CODE CONTINUES ⬇️
    class_info = conn.execute(
        "SELECT * FROM classes WHERE id=?", (class_id,)
    ).fetchone()

    students = conn.execute(
        "SELECT * FROM students WHERE class_id=?", (class_id,)
    ).fetchall()

    if request.method == "POST":
        date = today  # reuse today

        for student in students:
            status = request.form.get(f"status_{student['id']}")
            if status:
                conn.execute("""
                    INSERT OR REPLACE INTO attendance
                    (date, class_id, student_id, status)
                    VALUES (?, ?, ?, ?)
                """, (date, class_id, student["id"], status))

        conn.commit()
        conn.close()
        flash("Attendance saved successfully", "success")
        return redirect(url_for("teacher_dashboard"))

    conn.close()
    return render_template(
        "take_attendance.html",
        class_info=class_info,
        students=students
    )



@app.route("/teacher/attendance_history")
def teacher_attendance_history():
    if session.get("is_admin") or not session.get("user_id"):
        return redirect(url_for("login"))

    conn = get_db_connection()

    records = conn.execute("""
        SELECT 
            a.date,
            c.name AS class_name,
            c.section,
            s.name AS student_name,
            s.roll_no,
            a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        JOIN classes c ON a.class_id = c.id
        JOIN teacher_classes tc ON tc.class_id = c.id
        WHERE tc.teacher_id = ?
        ORDER BY a.date DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    return render_template(
        "teacher_attendance_history.html",
        records=records
    )


# ======================================================
# RUN APP
# ======================================================
import os

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
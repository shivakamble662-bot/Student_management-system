from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            course TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students ORDER BY id ASC"
    ).fetchall()
    conn.close()

    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]
        age = request.form["age"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO students
            (name, email, phone, course, age)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, course, age))

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add_student.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    conn = get_db_connection()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]
        age = request.form["age"]

        conn.execute("""
            UPDATE students
            SET name = ?, email = ?, phone = ?, course = ?, age = ?
            WHERE id = ?
        """, (name, email, phone, course, age, id))

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()

    conn.close()

    return render_template("edit_student.html", student=student)


@app.route("/delete/<int:id>")
def delete_student(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM students WHERE id = ?", (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/search")
def search():

    keyword = request.args.get("keyword", "")

    conn = get_db_connection()

    students = conn.execute("""
        SELECT * FROM students
        WHERE name LIKE ?
        OR email LIKE ?
        OR course LIKE ?
    """, (
        "%" + keyword + "%",
        "%" + keyword + "%",
        "%" + keyword + "%"
    )).fetchall()

    conn.close()

    return render_template(
        "index.html",
        students=students,
        keyword=keyword
    )


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
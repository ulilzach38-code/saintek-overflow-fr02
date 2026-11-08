from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_connection
from question import validate_question, save_question, get_all_questions
import os
import secrets

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "ganti-secret-key-untuk-demo")


@app.before_request
def prepare_csrf_token():
    """Membuat token CSRF untuk melindungi formulir dari pengiriman lintas situs."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)


@app.route("/demo-login", methods=["GET", "POST"])
def demo_login():
    """Simulasi login. Tidak menggantikan sistem autentikasi sungguhan."""
    if request.method == "POST":
        student_name = request.form.get("student_name", "").strip()

        if not student_name:
            flash("Nama mahasiswa wajib diisi.", "error")
            return redirect(url_for("demo_login"))

        # ID 1 adalah akun demo yang dibuat pada file SQL.
        session["user_id"] = 1
        session["student_name"] = student_name[:100]
        flash(f"Halo, {session['student_name']}! Kamu sudah masuk ke mode demo.", "success")
        return redirect(url_for("index"))

    return render_template("demo_login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Kamu sudah keluar dari mode demo.", "success")
    return redirect(url_for("demo_login"))


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("demo_login"))

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT category_id, category_name FROM categories ORDER BY category_name"
            )
            categories = cursor.fetchall()
    finally:
        connection.close()

    questions = get_all_questions()
    return render_template(
        "index.html",
        categories=categories,
        questions=questions,
        student_name=session.get("student_name", "Mahasiswa"),
        csrf_token=session["csrf_token"],
    )


@app.route("/submit", methods=["POST"])
def submit():
    if "user_id" not in session:
        flash("Silakan masuk ke mode demo terlebih dahulu.", "error")
        return redirect(url_for("demo_login"))

    submitted_token = request.form.get("csrf_token", "")
    if not secrets.compare_digest(submitted_token, session.get("csrf_token", "")):
        flash("Permintaan tidak valid. Muat ulang halaman lalu coba lagi.", "error")
        return redirect(url_for("index"))

    question_data = {
        "title": request.form.get("title", "").strip(),
        "description": request.form.get("description", "").strip(),
        "category_id": request.form.get("category_id", "").strip(),
        "tags": request.form.get("tags", "").strip(),
    }

    errors = validate_question(question_data)
    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("index"))

    try:
        save_question(question_data, session["user_id"])
        flash("Pertanyaan berhasil diajukan!", "success")
    except Exception:
        app.logger.exception("Gagal menyimpan pertanyaan")
        flash("Pertanyaan belum berhasil disimpan. Periksa koneksi database.", "error")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

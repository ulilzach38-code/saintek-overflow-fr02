from database import get_connection


def validate_question(question_data):
    """Memeriksa kelengkapan dan batas panjang input pertanyaan."""
    errors = []

    title = question_data["title"]
    description = question_data["description"]
    category_id = question_data["category_id"]
    tags = question_data["tags"]

    if not title:
        errors.append("Judul pertanyaan wajib diisi.")
    elif len(title) < 5:
        errors.append("Judul minimal terdiri dari 5 karakter.")
    elif len(title) > 150:
        errors.append("Judul maksimal terdiri dari 150 karakter.")

    if not description:
        errors.append("Deskripsi pertanyaan wajib diisi.")
    elif len(description) < 10:
        errors.append("Deskripsi minimal terdiri dari 10 karakter.")
    elif len(description) > 5000:
        errors.append("Deskripsi maksimal terdiri dari 5000 karakter.")

    if not category_id.isdigit():
        errors.append("Silakan pilih kategori yang tersedia.")

    if len(tags) > 255:
        errors.append("Tag maksimal terdiri dari 255 karakter.")

    if category_id.isdigit() and not category_exists(int(category_id)):
        errors.append("Kategori yang dipilih tidak ditemukan.")

    return errors


def category_exists(category_id):
    """Memastikan kategori benar-benar tersedia di database."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT category_id FROM categories WHERE category_id = %s",
                (category_id,),
            )
            return cursor.fetchone() is not None
    finally:
        connection.close()


def save_question(question_data, user_id):
    """Menyimpan pertanyaan baru dengan parameterized query."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO questions
                    (user_id, category_id, title, description, tags, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (
                    user_id,
                    int(question_data["category_id"]),
                    question_data["title"],
                    question_data["description"],
                    question_data["tags"],
                    "Open",
                ),
            )
    finally:
        connection.close()


def get_all_questions():
    """Mengambil daftar pertanyaan terbaru beserta nama kategori dan penulis."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT
                    q.question_id,
                    q.title,
                    q.description,
                    q.tags,
                    q.status,
                    q.created_at,
                    c.category_name,
                    u.username
                FROM questions AS q
                JOIN categories AS c ON q.category_id = c.category_id
                JOIN users AS u ON q.user_id = u.user_id
                ORDER BY q.created_at DESC, q.question_id DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        connection.close()

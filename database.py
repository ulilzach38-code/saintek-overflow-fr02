import os
import pymysql
from pymysql.cursors import DictCursor


def get_connection():
    """Membuka koneksi ke database MySQL."""
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "saintek_overflow"),
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=True,
    )

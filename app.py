import os
import secrets

import psycopg
from psycopg.rows import dict_row
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")
APP_TITLE = os.getenv("APP_TITLE", "Розклад занять")
APP_VERSION = os.getenv("APP_VERSION", "1.0")
STATUSES = {"new", "in_progress", "done"}


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def is_admin_request():
    header = request.headers.get("Authorization", "")
    prefix = "Bearer "

    if not header.startswith(prefix) or not ADMIN_TOKEN:
        return False

    provided_token = header[len(prefix):].strip()
    return secrets.compare_digest(provided_token, ADMIN_TOKEN)


@app.get("/")
def index():
    return jsonify({
        "application": APP_TITLE,
        "version": APP_VERSION,
        "status": "running",
        "endpoints": ["/health", "/api/lessons", "/api/admin/stats"]
    })


@app.get("/health")
def health():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 AS ok;")
                cursor.fetchone()
        return jsonify({"status": "ok", "database": "ok",
                        "version": APP_VERSION}), 200
    except Exception:
        return jsonify({"status": "degraded", "database": "error",
                        "version": APP_VERSION}), 503


@app.get("/api/lessons")
def get_lessons():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, subject, room, status, created_at
                FROM lessons
                ORDER BY id DESC;
                """
            )
            lessons = cursor.fetchall()
    return jsonify(lessons)


@app.post("/api/lessons")
def create_lesson():
    if not is_admin_request():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    subject = str(data.get("subject", "")).strip()
    room = str(data.get("room", "")).strip()
    status = str(data.get("status", "new")).strip()

    if not subject or not room:
        return jsonify({"error": "subject and room are required"}), 400

    if status not in STATUSES:
        return jsonify({"error": "invalid status"}), 400

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO lessons (subject, room, status)
                VALUES (%s, %s, %s)
                RETURNING id, subject, room, status, created_at;
                """,
                (subject, room, status)
            )
            lesson = cursor.fetchone()

    return jsonify(lesson), 201


@app.get("/api/admin/stats")
def admin_stats():
    if not is_admin_request():
        return jsonify({"error": "Unauthorized"}), 401

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT status, COUNT(*) AS count
                FROM lessons
                GROUP BY status
                ORDER BY status;
                """
            )
            stats = cursor.fetchall()

    return jsonify({"application": APP_TITLE, "version": APP_VERSION,
                    "statistics": stats})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)

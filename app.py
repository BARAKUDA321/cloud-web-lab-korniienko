import os
from flask import Flask, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

APP_TITLE = os.getenv(
    "APP_TITLE",
    "Розклад занять"
)

APP_MESSAGE = os.getenv(
    "APP_MESSAGE",
    "Застосунок запущено локально"
)


@app.route("/")
def index():
    return f"""
    <!doctype html>
    <html lang="uk">
    <head>
        <meta charset="utf-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
        <title>{APP_TITLE}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 760px;
                margin: 50px auto;
                padding: 24px;
                line-height: 1.5;
            }}
            .card {{
                border: 1px solid #ddd;
                border-radius: 14px;
                padding: 24px;
            }}
            code {{
                background: #f3f3f3;
                padding: 3px 6px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>{APP_TITLE}</h1>
            <p>{APP_MESSAGE}</p>
            <p>Вебзастосунок для перегляду розкладу занять групи.</p>
            <p>Розклад (JSON): <code>/api/lessons</code></p>
            <p>API: <code>/api/info</code></p>
            <p>Health: <code>/health</code></p>
        </div>
    </body>
    </html>
    """


@app.route("/api/info")
def api_info():
    return jsonify({
        "application": APP_TITLE,
        "platform": "cloud",
        "runtime": "python-flask",
        "status": "running",
           "student": "Корнієнко",
              "version": "1.1"
    })


@app.route("/api/lessons")
def lessons():
    return jsonify([
        {"id": 1, "day": "Понеділок", "time": "08:30",
         "subject": "Хмарні технології та обчислення"},
        {"id": 2, "day": "Вівторок", "time": "10:10",
         "subject": "Бази даних"},
        {"id": 3, "day": "Середа", "time": "11:50",
         "subject": "Вебтехнології"}
    ])


@app.route("/api/env")
def env_info():
    return jsonify({
        "app_title": APP_TITLE,
        "environment": "cloud"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    }), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
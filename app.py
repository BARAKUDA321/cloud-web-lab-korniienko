from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <h1>CI/CD Cloud App</h1>
    <p>Версія застосунку розгортається автоматично.</p>
    """


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    }), 200


@app.route("/api/lessons")
def lessons():
    return jsonify([
        {"id": 1, "subject": "Хмарні технології", "group": "ПС-36", "time": "08:30"},
        {"id": 2, "subject": "Бази даних", "group": "ПС-36", "time": "10:10"},
        {"id": 3, "subject": "Програмування", "group": "ПС-36", "time": "11:50"}
    ])


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

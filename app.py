
from flask import Flask, jsonify, render_template, request
from pathlib import Path
import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "finance.db"

app = Flask(__name__)
DATA_DIR.mkdir(exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                finance_type TEXT NOT NULL
                    CHECK(finance_type IN ('personal', 'business')),
                transaction_date TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                transaction_type TEXT NOT NULL
                    CHECK(transaction_type IN ('income', 'expense')),
                amount REAL NOT NULL CHECK(amount > 0),
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def get_transactions(finance_type=None):
    with get_connection() as conn:
        if finance_type:
            rows = conn.execute(
                """SELECT * FROM transactions
                   WHERE finance_type = ?
                   ORDER BY transaction_date DESC, id DESC""",
                (finance_type,)
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM transactions
                   ORDER BY transaction_date DESC, id DESC"""
            ).fetchall()

    return [dict(row) for row in rows]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "Finance Intelligence AI",
        "database": DB_PATH.exists()
    })


@app.route("/api/transactions", methods=["GET", "POST"])
def transactions():
    if request.method == "GET":
        finance_type = request.args.get("finance_type")
        if finance_type and finance_type not in ("personal", "business"):
            return jsonify({"error": "Invalid finance_type"}), 400

        return jsonify({"transactions": get_transactions(finance_type)})

    payload = request.get_json(silent=True) or {}

    finance_type = payload.get("finance_type")
    transaction_date = payload.get("transaction_date")
    description = payload.get("description")
    category = payload.get("category")
    transaction_type = payload.get("transaction_type")

    try:
        amount = float(payload.get("amount", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Amount must be a valid number"}), 400

    if finance_type not in ("personal", "business"):
        return jsonify({"error": "Choose personal or business finance"}), 400

    if transaction_type not in ("income", "expense"):
        return jsonify({"error": "Choose income or expense"}), 400

    if not all(isinstance(value, str) and value.strip()
               for value in (transaction_date, description, category)):
        return jsonify({
            "error": "Date, description and category are required"
        }), 400

    try:
        parsed_date = pd.to_datetime(
            transaction_date, format="%Y-%m-%d", errors="raise"
        )
    except (ValueError, TypeError):
        return jsonify({"error": "Date must use YYYY-MM-DD format"}), 400

    if parsed_date.strftime("%Y-%m-%d") != transaction_date:
        return jsonify({"error": "Invalid transaction date"}), 400

    if not 0 < amount <= 1_000_000_000_000:
        return jsonify({"error": "Amount must be positive and within limit"}), 400

    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO transactions
               (finance_type, transaction_date, description, category,
                transaction_type, amount)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                finance_type,
                transaction_date,
                description.strip()[:200],
                category.strip()[:100],
                transaction_type,
                amount
            )
        )
        transaction_id = cursor.lastrowid

    return jsonify({
        "message": "Transaction saved successfully",
        "id": transaction_id
    }), 201


@app.route("/api/summary")
def summary():
    finance_type = request.args.get("finance_type")
    if finance_type and finance_type not in ("personal", "business"):
        return jsonify({"error": "Invalid finance_type"}), 400

    records = get_transactions(finance_type)
    income = sum(
        item["amount"] for item in records
        if item["transaction_type"] == "income"
    )
    expenses = sum(
        item["amount"] for item in records
        if item["transaction_type"] == "expense"
    )

    return jsonify({
        "finance_type": finance_type or "all",
        "transaction_count": len(records),
        "total_income": round(income, 2),
        "total_expenses": round(expenses, 2),
        "net_cash_flow": round(income - expenses, 2),
        "savings_rate_percent": round(
            ((income - expenses) / income * 100) if income else 0, 2
        )
    })


@app.route("/api/anomalies")
def anomalies():
    finance_type = request.args.get("finance_type")
    if finance_type and finance_type not in ("personal", "business"):
        return jsonify({"error": "Invalid finance_type"}), 400

    records = get_transactions(finance_type)
    expenses = [r for r in records if r["transaction_type"] == "expense"]

    if len(expenses) < 5:
        return jsonify({
            "message": "Add at least 5 expense transactions for anomaly analysis",
            "anomalies": []
        })

    frame = pd.DataFrame(expenses)
    model = IsolationForest(
        contamination="auto",
        random_state=42
    )
    predictions = model.fit_predict(frame[["amount"]])

    flagged = []
    for record, prediction in zip(expenses, predictions):
        if prediction == -1:
            flagged.append({
                "id": record["id"],
                "date": record["transaction_date"],
                "description": record["description"],
                "category": record["category"],
                "amount": record["amount"],
                "note": "Unusual amount detected; review this transaction"
            })

    return jsonify({
        "method": "IsolationForest",
        "transactions_analyzed": len(expenses),
        "anomalies": flagged
    })


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, port=5000)

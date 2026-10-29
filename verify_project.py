import sys
import compileall
from pathlib import Path

print("\n=== FINANCE INTELLIGENCE AI: FULL PROJECT CHECK ===\n")
root = Path(__file__).resolve().parent
failed = []

def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}" + (f" - {detail}" if detail else ""))
    if not condition:
        failed.append(name)

# 1. Python files and dependencies
python_files = list(root.rglob("*.py"))
python_files = [
    p for p in python_files
    if ".venv" not in p.parts and "__pycache__" not in p.parts
]
syntax_ok = all(compileall.compile_file(str(p), quiet=1) for p in python_files)
check("Python syntax", bool(python_files) and syntax_ok,
      f"{len(python_files)} Python file(s)")

try:
    import flask, pandas, sklearn, numpy
    check("Dependencies", True, "Flask, Pandas, Scikit-learn, NumPy")
except Exception as exc:
    check("Dependencies", False, str(exc))
    print("\nFix dependencies before continuing.")
    sys.exit(1)

# 2. Required project files
for name in [
    "app.py", "requirements.txt", ".gitignore",
    "templates/index.html", "static/style.css", "static/script.js"
]:
    check(f"File: {name}", (root / name).is_file())

# 3. Backend, database and APIs
try:
    import app as application
    application.initialize_database()
    client = application.app.test_client()

    response = client.get("/")
    check("Dashboard route", response.status_code == 200,
          f"HTTP {response.status_code}")

    if response.status_code == 200:
        page = response.get_data(as_text=True)
        check("HTML references CSS", "style.css" in page)
        check("HTML references JavaScript", "script.js" in page)

    response = client.get("/api/health")
    check("Health API", response.status_code == 200,
          f"HTTP {response.status_code}")
    if response.status_code == 200:
        check("Database health", response.json.get("database") is True)

    response = client.get("/api/summary")
    check("Summary API", response.status_code == 200,
          f"HTTP {response.status_code}")
    if response.status_code == 200:
        keys = {
            "total_income", "total_expenses",
            "net_cash_flow", "savings_rate_percent"
        }
        check("Summary fields", keys.issubset(response.json.keys()))

    response = client.get("/api/transactions")
    check("Transactions API", response.status_code == 200,
          f"HTTP {response.status_code}")
    if response.status_code == 200:
        check("Transactions response",
              isinstance(response.json.get("transactions"), list))

    response = client.get("/api/anomalies")
    check("Anomaly API", response.status_code == 200,
          f"HTTP {response.status_code}")

    response = client.get("/api/summary?finance_type=invalid")
    check("Invalid input validation", response.status_code == 400,
          f"HTTP {response.status_code}")

except Exception as exc:
    check("Backend/API tests", False, repr(exc))

print("\n=== RESULT ===")
if failed:
    print(f"{len(failed)} CHECK(S) FAILED:")
    for name in failed:
        print(" -", name)
    sys.exit(1)
else:
    print("ALL CHECKS PASSED")

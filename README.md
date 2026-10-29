# 💹 Finance Intelligence AI

### 🧠 AI-Powered Financial Analytics • Cash Flow Intelligence • Expense Anomaly Detection

<p align="center">
  <strong>Turn financial transactions into actionable insights.</strong>
</p>

<p align="center">
  A Python-powered financial intelligence platform for personal and business finance, combining interactive analytics, transaction management, and machine-learning-based expense anomaly detection.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-REST%20API-black?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange?logo=scikitlearn" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Status-Active-success" alt="Project Status">
</p>

---

## 🌟 Overview

**Finance Intelligence AI** is a web-based financial analytics application designed to help individuals and businesses understand their financial activity through structured transaction records, income and expense analysis, cash flow metrics, and machine-learning-assisted anomaly detection.

Built with Python, Flask, SQLite, Pandas, NumPy, and Scikit-learn, the platform provides a foundation for more informed financial management and future predictive analytics.

## ✨ Key Features

| Feature | Description |
|---|---|
| 💰 Financial Overview | Calculate income, expenses, net cash flow, and savings rate |
| 🧾 Transaction Management | Record and retrieve categorized financial transactions |
| 🏢 Personal & Business Finance | Organize transactions by finance type |
| 🧠 Expense Anomaly Detection | Flag potentially unusual expenses using Isolation Forest |
| 📊 Interactive Dashboard | Explore financial metrics through a web interface and charts |
| 🔌 REST API | Access transactions, summaries, health checks, and anomaly analysis |
| 🗄️ Persistent Storage | Store transaction data using SQLite |
| 🛡️ Input Validation | Reject invalid requests and validate transaction data |
| 🧪 Project Verification | Check core files, dependencies, routes, and API responses |

## 🖥️ Technology Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,flask,html,css,js,sqlite" alt="Technology stack icons">
</p>

| Layer | Technology |
|---|---|
| Language | Python |
| Backend | Flask |
| Data Analytics | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Visualization | Chart.js |
| Testing | Flask Test Client, Python verification script |

## 🏗️ System Architecture

```text
                   ┌────────────────────────┐
                   │        User            │
                   └───────────┬────────────┘
                               │
                               ▼
                   ┌────────────────────────┐
                   │   Web Dashboard        │
                   │ HTML • CSS • JavaScript│
                   └───────────┬────────────┘
                               │
                               ▼
                   ┌────────────────────────┐
                   │    Flask REST API      │
                   └───────────┬────────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
          ┌──────────────────┐   ┌──────────────────┐
          │ Financial        │   │ Anomaly Detection│
          │ Analytics        │   │ Isolation Forest │
          └─────────┬────────┘   └─────────┬────────┘
                    └──────────┬───────────┘
                               ▼
                   ┌────────────────────────┐
                   │    SQLite Database     │
                   └────────────────────────┘
```

## 📂 Project Structure

```text
Finance-Intelligence-AI/
│
├── app.py
├── verify_project.py
├── requirements.txt
├── .gitignore
├── .env.example
├── LICENSE
│
├── data/
│   └── finance.db
│
├── reports/
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

> The structure represents the core application. Keep the README updated as additional modules, tests, and documentation are added. Do not commit private financial databases or real credentials.

## ⚙️ Getting Started

### Prerequisites

- Python 3.13 or another compatible Python version
- pip package manager
- Visual Studio Code (recommended)

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd "Finance Intelligence AI"
```

Replace `YOUR_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Start the application

```powershell
python app.py
```

Open your browser and visit:

**http://127.0.0.1:5000**

## 🔌 API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Serve the dashboard |
| `GET` | `/api/health` | Check application and database health |
| `GET` | `/api/transactions` | Retrieve transaction records |
| `POST` | `/api/transactions` | Add a transaction |
| `GET` | `/api/summary` | Retrieve financial summary metrics |
| `GET` | `/api/anomalies` | Analyze potentially unusual expenses |

### 📦 Transaction Data

Transactions contain fields such as:

- Finance type: personal or business
- Date and description
- Category
- Transaction type: income or expense
- Amount

The API validates incoming data before database operations.

## 🧠 Machine Learning & Anomaly Detection

The anomaly detection component uses **Isolation Forest**, an unsupervised machine learning algorithm provided by Scikit-learn.

It analyzes expense amounts to identify transactions that may differ from typical spending patterns.

**Important:** An anomaly is a signal for review, not proof of fraud or an incorrect transaction. Results depend on data quality, transaction volume, and model configuration.

## 🧪 Run Project Verification

Run the included verification script:

```powershell
python verify_project.py
```

The current checks cover:

- Python syntax
- Required project files
- Installed dependencies
- Dashboard route and static asset references
- Database health
- Summary and transaction APIs
- Anomaly endpoint
- Invalid input validation

## 🔐 Security & Privacy

- Validate incoming transaction data.
- Use parameterized SQL queries for database access.
- Keep environment secrets and private financial records out of public repositories.
- Exclude virtual environments, local databases, and sensitive files through `.gitignore`.
- Use synthetic data for public demonstrations.
- Review machine learning results before making financial decisions.

## 🗺️ Roadmap

- [ ] Historical cash flow forecasting
- [ ] Monthly and annual financial report generation
- [ ] CSV transaction import and export
- [ ] Budget planning and spending alerts
- [ ] Expanded automated unit and integration tests
- [ ] Continuous integration with GitHub Actions
- [ ] Improved authentication and access control
- [ ] Production deployment configuration

*Roadmap items are planned enhancements and should not be interpreted as implemented features.*

## 🎯 Project Goals

Finance Intelligence AI aims to demonstrate practical skills in:

- Backend development with Python and Flask
- REST API design and validation
- Financial data processing and analytics
- Machine learning integration
- Database management
- Interactive web development
- Automated project verification
- Secure software development practices

## ⚠️ Disclaimer

This project is intended for educational, analytical, and demonstration purposes. It does not provide certified financial, tax, investment, or accounting advice. Anomaly detection results should be independently reviewed before action is taken.

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

<p align="center">
  <strong>💹 Finance Intelligence AI</strong><br>
  <em>Building smarter financial insights with data and AI.</em>
</p>
</Writing

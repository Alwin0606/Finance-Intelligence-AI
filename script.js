
const $ = (id) => document.getElementById(id);
let cashFlowChart = null;
let currentTransactions = [];

const money = (amount) => new Intl.NumberFormat("en-US", {
    style: "currency", currency: "USD", maximumFractionDigits: 2
}).format(amount || 0);

function selectedProfile() {
    return $("financeType").value;
}

function profileQuery() {
    return selectedProfile() === "all" ? "" : `?finance_type=${selectedProfile()}`;
}

async function api(url, options = {}) {
    const response = await fetch(url, options);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Request failed");
    return data;
}

function showToast(message) {
    const toast = $("toast");
    toast.textContent = message;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 3000);
}

function addInsight(title, message) {
    const item = document.createElement("div");
    item.className = "insight-item";
    const heading = document.createElement("strong");
    heading.textContent = title;
    const detail = document.createElement("p");
    detail.textContent = message;
    item.append(heading, detail);
    $("insights").appendChild(item);
}

function renderInsights(summary, transactions) {
    const container = $("insights");
    container.replaceChildren();

    if (!transactions.length) {
        const empty = document.createElement("div");
        empty.className = "empty-state";
        empty.textContent = "Add transactions to generate insights.";
        container.appendChild(empty);
        return;
    }

    if (summary.net_cash_flow < 0) {
        addInsight("Negative net cash flow", "Recorded expenses exceed recorded income. Review your budget.");
    } else {
        addInsight("Positive net cash flow", `Your recorded net cash flow is ${money(summary.net_cash_flow)}.`);
    }

    if (summary.total_income > 0) {
        addInsight("Savings rate", `${summary.savings_rate_percent}% of recorded income remains after expenses.`);
    } else {
        addInsight("Income needed", "Record income to calculate a meaningful savings rate.");
    }

    const expenses = transactions.filter(t => t.transaction_type === "expense");
    if (expenses.length >= 5) {
        try {
            const values = expenses.map(t => t.amount);
            const median = [...values].sort((a, b) => a - b)[Math.floor(values.length / 2)];
            const highSpends = expenses.filter(t => t.amount > median * 2);
            if (highSpends.length) {
                addInsight("Large transactions", `${highSpends.length} expense(s) exceed twice the median expense. This is a review signal, not proof of fraud.`);
            }
        } catch {
            addInsight("Expense review", "Review your recorded expenses regularly.");
        }
    } else {
        addInsight("AI anomaly analysis", "Record at least 5 expenses to enable the initial anomaly scan.");
    }
}

function renderTransactions(transactions) {
    const tbody = $("transactionRows");
    tbody.replaceChildren();

    if (!transactions.length) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        cell.colSpan = 5;
        cell.className = "empty-state";
        cell.textContent = "No transactions yet. Add your first transaction.";
        row.appendChild(cell);
        tbody.appendChild(row);
        return;
    }

    transactions.slice(0, 8).forEach(t => {
        const row = document.createElement("tr");
        const values = [
            t.description,
            t.transaction_type,
            t.category,
            t.transaction_date
        ];

        values.forEach((value, index) => {
            const cell = document.createElement("td");
            cell.textContent = value;
            if (index === 1) {
                const pill = document.createElement("span");
                pill.className = "type-pill";
                pill.textContent = value;
                cell.replaceChildren(pill);
            }
            row.appendChild(cell);
        });

        const amountCell = document.createElement("td");
        amountCell.className = t.transaction_type === "income" ? "amount-income" : "amount-expense";
        amountCell.textContent = `${t.transaction_type === "income" ? "+" : "−"}${money(t.amount)}`;
        row.appendChild(amountCell);
        tbody.appendChild(row);
    });
}

function renderChart(transactions) {
    const monthly = {};

    transactions.forEach(t => {
        const month = t.transaction_date.slice(0, 7);
        if (!monthly[month]) monthly[month] = { income: 0, expenses: 0 };
        if (t.transaction_type === "income") monthly[month].income += t.amount;
        else monthly[month].expenses += t.amount;
    });

    const labels = Object.keys(monthly).sort();
    const income = labels.map(m => monthly[m].income);
    const expenses = labels.map(m => monthly[m].expenses);

    if (cashFlowChart) cashFlowChart.destroy();

    cashFlowChart = new Chart($("cashFlowChart"), {
        type: "bar",
        data: {
            labels,
            datasets: [
                { label: "Income", data: income, backgroundColor: "#65e6b2", borderRadius: 5 },
                { label: "Expenses", data: expenses, backgroundColor: "#ff8793", borderRadius: 5 }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: "#aab6c9", usePointStyle: true, boxWidth: 8 } }
            },
            scales: {
                x: { ticks: { color: "#8b98ad" }, grid: { display: false } },
                y: { beginAtZero: true, ticks: { color: "#8b98ad" }, grid: { color: "#263044" } }
            }
        }
    });
}

async function loadDashboard() {
    try {
        const [summary, transactionData] = await Promise.all([
            api(`/api/summary${profileQuery()}`),
            api(`/api/transactions${profileQuery()}`)
        ]);

        currentTransactions = transactionData.transactions;
        $("totalIncome").textContent = money(summary.total_income);
        $("totalExpenses").textContent = money(summary.total_expenses);
        $("netCashFlow").textContent = money(summary.net_cash_flow);
        $("savingsRate").textContent = `${summary.savings_rate_percent}%`;

        renderTransactions(currentTransactions);
        renderChart(currentTransactions);
        renderInsights(summary, currentTransactions);
    } catch (error) {
        showToast(`Unable to load dashboard: ${error.message}`);
    }
}

function openModal() {
    $("formError").textContent = "";
    $("transactionForm").reset();
    $("transactionForm").elements.finance_type.value =
        selectedProfile() === "all" ? "personal" : selectedProfile();
    $("transactionForm").elements.transaction_date.value =
        new Date().toLocaleDateString("en-CA");
    $("transactionModal").classList.remove("hidden");
}

function closeModal() {
    $("transactionModal").classList.add("hidden");
}

$("addTransactionBtn").addEventListener("click", openModal);
$("closeModal").addEventListener("click", closeModal);

$("transactionModal").addEventListener("click", event => {
    if (event.target === $("transactionModal")) closeModal();
});

$("transactionForm").addEventListener("submit", async event => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = Object.fromEntries(new FormData(form).entries());
    payload.amount = Number(payload.amount);

    try {
        await api("/api/transactions", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        closeModal();
        await loadDashboard();
        showToast("Transaction saved successfully.");
    } catch (error) {
        $("formError").textContent = error.message;
    }
});

$("financeType").addEventListener("change", loadDashboard);

$("viewAllBtn").addEventListener("click", () => {
    $("transactionRows").replaceChildren();
    renderTransactions(currentTransactions);
    showToast(`${currentTransactions.length} transaction(s) loaded.`);
});

document.querySelectorAll(".nav-item").forEach(button => {
    button.addEventListener("click", () => {
        document.querySelectorAll(".nav-item").forEach(item => item.classList.remove("active"));
        button.classList.add("active");

        const views = {
            overview: "Finance Overview",
            transactions: "Transactions",
            analytics: "AI Analytics",
            forecast: "Cash Flow",
            reports: "Financial Reports"
        };
        $("pageTitle").textContent = views[button.dataset.view] || "Finance Overview";

        if (button.dataset.view === "analytics") {
            api(`/api/anomalies${profileQuery()}`)
                .then(data => showToast(
                    data.anomalies?.length
                        ? `${data.anomalies.length} unusual transaction(s) flagged.`
                        : data.message || "No unusual transactions flagged."
                ))
                .catch(error => showToast(error.message));
        } else if (button.dataset.view === "forecast") {
            showToast("Forecasting module is planned for the next phase.");
        } else if (button.dataset.view === "reports") {
            showToast("Downloadable reports are planned for the next phase.");
        } else if (button.dataset.view === "transactions") {
            $("transactionRows").scrollIntoView({ behavior: "smooth", block: "center" });
        } else {
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    });
});

loadDashboard();

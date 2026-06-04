# 💰 StudyFund — Student Money Management App

A full-featured personal finance web app built for students, powered by Python, Flask, and PostgreSQL.

---

## Features

| Module | Description |
|---|---|
| 📋 **Budget Planner** | Allocate monthly income across categories, track spending vs. budget |
| 🎯 **Savings Goals** | Create goals with targets, deposit funds, track % progress |
| 🧾 **Expense Tracker** | Log expenses by category, filter, paginate, chart breakdowns |
| 📚 **Financial Education** | 6 articles on budgeting, saving, investing, debt & side hustles |
| 🚀 **Investment Simulator** | Compound interest calculator with real vs. nominal chart |

---

## Tech Stack

- **Backend**: Python 3.11, Flask 3.0, Flask-SQLAlchemy, Flask-Login
- **Database**: PostgreSQL 15
- **Frontend**: Jinja2 templates, Chart.js, vanilla CSS/JS (no frontend framework)
- **Auth**: Flask-Login with bcrypt password hashing (Werkzeug)


---

## Manual Setup (Local Dev)

### 1. Prerequisites
- Python 3.10+
- PostgreSQL running locally

### 2. Create database
```sql
psql -U postgres
CREATE DATABASE student_finance;
\q
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
# Option A: Export variables
export DATABASE_URL="postgresql://postgres:password@localhost:5432/student_finance"
export SECRET_KEY="your-secret-key"

# Option B: Create a .env file and use python-dotenv
```

### 5. Run the app
```bash
python app.py
```

Open **http://localhost:5000**

---

## Project Structure

```
student-finance/
├── app.py                  # App factory, blueprint registration
├── config.py               # Configuration (DB URL, secret key)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── models/
│   ├── user.py             # User model + login_manager loader
│   ├── budget.py           # Budget model (category, amount, month)
│   ├── savings.py          # SavingsGoal model
│   ├── expense.py          # Expense model
│   └── education.py        # Article model + seed data
│
├── routes/
│   ├── auth.py             # /register, /login, /logout
│   ├── dashboard.py        # /dashboard
│   ├── budget.py           # /budget, /budget/add, /budget/delete/<id>
│   ├── savings.py          # /savings, /savings/add, /savings/deposit/<id>
│   ├── expenses.py         # /expenses, /expenses/add, /expenses/delete/<id>
│   ├── education.py        # /education, /education/<id>
│   └── simulator.py        # /simulator, /simulator/calculate (JSON API)
│
└── templates/
    ├── base.html           # Sidebar layout, flash messages, modals
    ├── landing.html        # Public homepage
    ├── auth/               # login.html, register.html
    ├── dashboard/          # home.html
    ├── budget/             # index.html
    ├── savings/            # index.html
    ├── expenses/           # index.html
    ├── education/          # index.html, article.html
    └── simulator/          # index.html
```

---

## Database Schema

| Table | Key Columns |
|---|---|
| `users` | id, username, email, password_hash, monthly_income |
| `budgets` | id, user_id, category, allocated_amount, month, year |
| `savings_goals` | id, user_id, name, target_amount, current_amount, target_date, completed |
| `expenses` | id, user_id, description, amount, category, date, note |
| `articles` | id, title, summary, content, category, read_time, difficulty |

Tables are auto-created on first run via `db.create_all()`. Article seed data is inserted once.

---

## Expense / Budget Categories

Housing · Food & Dining · Transportation · Education · Entertainment · Health · Clothing · Utilities · Personal Care · Savings · Other

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql://postgres:password@localhost:5432/student_finance` | PostgreSQL connection string |
| `SECRET_KEY` | `student-finance-secret-key-2024` | Flask session secret (change in production!) |

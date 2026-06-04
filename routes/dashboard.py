from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.budget import Budget
from models.savings import SavingsGoal
from models.expense import Expense
from datetime import datetime
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def home():
    now = datetime.utcnow()
    month, year = now.month, now.year

    # Budget summary
    budgets = Budget.query.filter_by(user_id=current_user.id, month=month, year=year).all()
    total_budgeted = sum(b.allocated_amount for b in budgets)

    # Expenses this month
    expenses = Expense.query.filter_by(user_id=current_user.id).filter(
        func.extract('month', Expense.date) == month,
        func.extract('year', Expense.date) == year
    ).all()
    total_spent = sum(e.amount for e in expenses)

    # Category breakdown
    category_spending = {}
    for e in expenses:
        category_spending[e.category] = category_spending.get(e.category, 0) + e.amount

    # Budget vs spending per category
    budget_data = []
    for b in budgets:
        spent = category_spending.get(b.category, 0)
        budget_data.append({
            'category': b.category,
            'allocated': b.allocated_amount,
            'spent': spent,
            'remaining': max(b.allocated_amount - spent, 0),
            'percentage': min(round((spent / b.allocated_amount * 100) if b.allocated_amount > 0 else 0, 1), 100),
            'icon': Expense.CATEGORY_ICONS.get(b.category, '📦')
        })

    # Savings goals
    savings_goals = SavingsGoal.query.filter_by(user_id=current_user.id, completed=False).limit(3).all()

    # Recent expenses
    recent_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).limit(5).all()

    return render_template('dashboard/home.html',
        total_budgeted=total_budgeted,
        total_spent=total_spent,
        remaining=max(total_budgeted - total_spent, 0),
        budget_data=budget_data,
        savings_goals=savings_goals,
        recent_expenses=recent_expenses,
        month_name=now.strftime('%B %Y'),
        income=current_user.monthly_income
    )

@dashboard_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        income = request.form.get('monthly_income', 0)
        try:
            current_user.monthly_income = float(income)
            db.session.commit()
            flash('Income updated successfully!', 'success')
        except ValueError:
            flash('Invalid income value.', 'error')
        return redirect(url_for('dashboard.home'))
    return redirect(url_for('dashboard.home'))

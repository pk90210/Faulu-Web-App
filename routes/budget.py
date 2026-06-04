from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.budget import Budget
from models.expense import Expense
from datetime import datetime
from sqlalchemy import func

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/budget')
@login_required
def index():
    now = datetime.utcnow()
    month = int(request.args.get('month', now.month))
    year = int(request.args.get('year', now.year))

    budgets = Budget.query.filter_by(user_id=current_user.id, month=month, year=year).all()
    expenses = Expense.query.filter_by(user_id=current_user.id).filter(
        func.extract('month', Expense.date) == month,
        func.extract('year', Expense.date) == year
    ).all()

    spending_by_cat = {}
    for e in expenses:
        spending_by_cat[e.category] = spending_by_cat.get(e.category, 0) + e.amount

    budget_items = []
    for b in budgets:
        spent = spending_by_cat.get(b.category, 0)
        budget_items.append({
            'id': b.id,
            'category': b.category,
            'allocated': b.allocated_amount,
            'spent': spent,
            'remaining': max(b.allocated_amount - spent, 0),
            'percentage': min(round((spent / b.allocated_amount * 100) if b.allocated_amount > 0 else 0, 1), 100),
            'icon': Expense.CATEGORY_ICONS.get(b.category, '📦'),
            'over_budget': spent > b.allocated_amount
        })

    total_allocated = sum(b.allocated_amount for b in budgets)
    total_spent = sum(spending_by_cat.get(b.category, 0) for b in budgets)

    from datetime import date
    months = []
    for i in range(-3, 4):
        m = month + i
        y = year
        while m < 1: m += 12; y -= 1
        while m > 12: m -= 12; y += 1
        months.append({'month': m, 'year': y, 'label': date(y, m, 1).strftime('%b %Y')})

    return render_template('budget/index.html',
        budget_items=budget_items,
        categories=Budget.CATEGORIES,
        total_allocated=total_allocated,
        total_spent=total_spent,
        current_month=month,
        current_year=year,
        months=months,
        income=current_user.monthly_income
    )

@budget_bp.route('/budget/add', methods=['POST'])
@login_required
def add():
    category = request.form.get('category')
    amount = request.form.get('amount')
    month = int(request.form.get('month', datetime.utcnow().month))
    year = int(request.form.get('year', datetime.utcnow().year))

    if not category or not amount:
        flash('Category and amount are required.', 'error')
        return redirect(url_for('budget.index'))

    existing = Budget.query.filter_by(
        user_id=current_user.id, category=category, month=month, year=year
    ).first()

    if existing:
        existing.allocated_amount = float(amount)
        flash(f'Updated {category} budget.', 'success')
    else:
        budget = Budget(
            user_id=current_user.id,
            category=category,
            allocated_amount=float(amount),
            month=month,
            year=year
        )
        db.session.add(budget)
        flash(f'Added {category} budget.', 'success')

    db.session.commit()
    return redirect(url_for('budget.index', month=month, year=year))

@budget_bp.route('/budget/delete/<int:budget_id>', methods=['POST'])
@login_required
def delete(budget_id):
    budget = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first_or_404()
    db.session.delete(budget)
    db.session.commit()
    flash('Budget category removed.', 'success')
    return redirect(url_for('budget.index'))

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.expense import Expense
from models.budget import Budget
from datetime import datetime, date
from sqlalchemy import func

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/expenses')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category', '')
    month_filter = request.args.get('month', '')

    query = Expense.query.filter_by(user_id=current_user.id)

    if category_filter:
        query = query.filter_by(category=category_filter)
    if month_filter:
        try:
            year, month = map(int, month_filter.split('-'))
            query = query.filter(
                func.extract('month', Expense.date) == month,
                func.extract('year', Expense.date) == year
            )
        except (ValueError, AttributeError):
            pass

    expenses = query.order_by(Expense.date.desc()).paginate(page=page, per_page=15, error_out=False)

    # Stats
    now = datetime.utcnow()
    month_expenses = Expense.query.filter_by(user_id=current_user.id).filter(
        func.extract('month', Expense.date) == now.month,
        func.extract('year', Expense.date) == now.year
    ).all()
    monthly_total = sum(e.amount for e in month_expenses)

    category_totals = {}
    for e in month_expenses:
        category_totals[e.category] = category_totals.get(e.category, 0) + e.amount

    return render_template('expenses/index.html',
        expenses=expenses,
        categories=Expense.CATEGORY_ICONS,
        category_filter=category_filter,
        monthly_total=monthly_total,
        category_totals=category_totals,
        month_names=[(now.year, now.month)]
    )

@expenses_bp.route('/expenses/add', methods=['POST'])
@login_required
def add():
    description = request.form.get('description', '').strip()
    amount = request.form.get('amount')
    category = request.form.get('category')
    expense_date = request.form.get('date')
    note = request.form.get('note', '').strip()

    if not all([description, amount, category]):
        flash('Description, amount, and category are required.', 'error')
        return redirect(url_for('expenses.index'))

    expense = Expense(
        user_id=current_user.id,
        description=description,
        amount=float(amount),
        category=category,
        note=note if note else None
    )
    if expense_date:
        try:
            expense.date = datetime.strptime(expense_date, '%Y-%m-%d').date()
        except ValueError:
            expense.date = date.today()

    db.session.add(expense)
    db.session.commit()
    flash(f'Expense "{description}" added.', 'success')
    return redirect(url_for('expenses.index'))

@expenses_bp.route('/expenses/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete(expense_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted.', 'success')
    return redirect(url_for('expenses.index'))

@expenses_bp.route('/expenses/chart-data')
@login_required
def chart_data():
    now = datetime.utcnow()
    expenses = Expense.query.filter_by(user_id=current_user.id).filter(
        func.extract('month', Expense.date) == now.month,
        func.extract('year', Expense.date) == now.year
    ).all()

    categories = {}
    for e in expenses:
        categories[e.category] = categories.get(e.category, 0) + e.amount

    return jsonify({
        'labels': list(categories.keys()),
        'data': list(categories.values()),
        'icons': [Expense.CATEGORY_ICONS.get(c, '📦') for c in categories.keys()]
    })

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.savings import SavingsGoal
from datetime import datetime

savings_bp = Blueprint('savings', __name__)

@savings_bp.route('/savings')
@login_required
def index():
    active_goals = SavingsGoal.query.filter_by(user_id=current_user.id, completed=False).all()
    completed_goals = SavingsGoal.query.filter_by(user_id=current_user.id, completed=True).all()
    total_saved = sum(g.current_amount for g in active_goals)
    total_target = sum(g.target_amount for g in active_goals)
    return render_template('savings/index.html',
        active_goals=active_goals,
        completed_goals=completed_goals,
        total_saved=total_saved,
        total_target=total_target
    )

@savings_bp.route('/savings/add', methods=['POST'])
@login_required
def add():
    name = request.form.get('name', '').strip()
    target = request.form.get('target_amount')
    current = request.form.get('current_amount', 0)
    target_date = request.form.get('target_date')
    icon = request.form.get('icon', '🎯')
    color = request.form.get('color', '#4CAF50')

    if not name or not target:
        flash('Name and target amount are required.', 'error')
        return redirect(url_for('savings.index'))

    goal = SavingsGoal(
        user_id=current_user.id,
        name=name,
        target_amount=float(target),
        current_amount=float(current) if current else 0.0,
        icon=icon,
        color=color
    )
    if target_date:
        try:
            goal.target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        except ValueError:
            pass

    db.session.add(goal)
    db.session.commit()
    flash(f'Goal "{name}" created! 🎯', 'success')
    return redirect(url_for('savings.index'))

@savings_bp.route('/savings/deposit/<int:goal_id>', methods=['POST'])
@login_required
def deposit(goal_id):
    goal = SavingsGoal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    amount = float(request.form.get('amount', 0))
    if amount <= 0:
        flash('Please enter a valid amount.', 'error')
        return redirect(url_for('savings.index'))

    goal.current_amount += amount
    if goal.current_amount >= goal.target_amount:
        goal.completed = True
        flash(f'🎉 Congratulations! You\'ve reached your "{goal.name}" goal!', 'success')
    else:
        flash(f'Added KES {amount:,.2f} to "{goal.name}". {goal.progress_percentage}% complete!', 'success')

    db.session.commit()
    return redirect(url_for('savings.index'))

@savings_bp.route('/savings/delete/<int:goal_id>', methods=['POST'])
@login_required
def delete(goal_id):
    goal = SavingsGoal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    name = goal.name
    db.session.delete(goal)
    db.session.commit()
    flash(f'Goal "{name}" deleted.', 'success')
    return redirect(url_for('savings.index'))

from extensions import db
from datetime import datetime

class Budget(db.Model):
    __tablename__ = 'budgets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    allocated_amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    CATEGORIES = [
        'Housing', 'Food & Dining', 'Transportation', 'Education',
        'Entertainment', 'Health', 'Clothing', 'Utilities',
        'Personal Care', 'Savings', 'Other'
    ]

    def __repr__(self):
        return f'<Budget {self.category}: {self.allocated_amount}>'

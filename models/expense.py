from extensions import db
from datetime import datetime

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    CATEGORY_ICONS = {
        'Housing': '🏠', 'Food & Dining': '🍔', 'Transportation': '🚌',
        'Education': '📚', 'Entertainment': '🎬', 'Health': '💊',
        'Clothing': '👕', 'Utilities': '💡', 'Personal Care': '🧴',
        'Savings': '💰', 'Other': '📦'
    }

    @property
    def category_icon(self):
        return self.CATEGORY_ICONS.get(self.category, '📦')

    def __repr__(self):
        return f'<Expense {self.description}: {self.amount}>'

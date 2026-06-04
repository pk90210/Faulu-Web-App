from extensions import db
from datetime import datetime

class SavingsGoal(db.Model):
    __tablename__ = 'savings_goals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    target_date = db.Column(db.Date, nullable=True)
    icon = db.Column(db.String(50), default='🎯')
    color = db.Column(db.String(20), default='#4CAF50')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    @property
    def progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return min(round((self.current_amount / self.target_amount) * 100, 1), 100)

    @property
    def remaining(self):
        return max(self.target_amount - self.current_amount, 0)

    def __repr__(self):
        return f'<SavingsGoal {self.name}: {self.current_amount}/{self.target_amount}>'

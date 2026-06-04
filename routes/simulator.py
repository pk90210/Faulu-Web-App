from flask import Blueprint, render_template, request, jsonify
import math

simulator_bp = Blueprint('simulator', __name__)

@simulator_bp.route('/simulator')
def index():
    return render_template('simulator/index.html')

@simulator_bp.route('/simulator/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    initial = float(data.get('initial', 0))
    monthly = float(data.get('monthly', 0))
    rate = float(data.get('rate', 10)) / 100
    years = int(data.get('years', 10))
    inflation = float(data.get('inflation', 5)) / 100

    monthly_rate = rate / 12
    results = []
    balance = initial

    for month in range(1, years * 12 + 1):
        balance = balance * (1 + monthly_rate) + monthly
        if month % 12 == 0:
            year_num = month // 12
            inflation_factor = (1 + inflation) ** year_num
            real_value = balance / inflation_factor
            results.append({
                'year': year_num,
                'nominal': round(balance, 2),
                'real': round(real_value, 2)
            })

    total_invested = initial + (monthly * 12 * years)
    final_balance = results[-1]['nominal'] if results else initial
    total_interest = final_balance - total_invested

    return jsonify({
        'results': results,
        'summary': {
            'final_balance': round(final_balance, 2),
            'total_invested': round(total_invested, 2),
            'total_interest': round(total_interest, 2),
            'growth_multiple': round(final_balance / total_invested, 2) if total_invested > 0 else 1
        }
    })

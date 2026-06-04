from datetime import datetime
from extensions import db
# import requests

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    read_time = db.Column(db.Integer, default=5)
    icon = db.Column(db.String(50), default='📖')
    difficulty = db.Column(db.String(20), default='Beginner')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def seed_articles():
    from app import db

    if db.session.execute(db.select(Article)).first() is not None:
        return

    articles = [
        Article(
            title="The 50/30/20 Budget Rule for Students",
            summary="Learn the simplest budgeting framework that allocates your income across needs, wants, and savings.",
            content="""<h3>What is the 50/30/20 Rule?</h3>
<p>The 50/30/20 rule is a simple budgeting method that divides your after-tax income into three categories:</p>
<ul>
<li><strong>50% for Needs</strong> — rent, tuition, groceries, utilities, transport</li>
<li><strong>30% for Wants</strong> — eating out, streaming services, hobbies, travel</li>
<li><strong>20% for Savings</strong> — emergency fund, investments, debt repayment</li>
</ul>
<h3>Why It Works for Students</h3>
<p>As a student, income can be irregular (part-time jobs, allowances, scholarships). The 50/30/20 rule adapts to any income level and keeps things simple. Even if you earn KES 10,000/month, you can apply this framework.</p>
<h3>Practical Example</h3>
<p>Monthly income: KES 15,000<br>Needs (50%): KES 7,500 — rent, food, transport<br>Wants (30%): KES 4,500 — entertainment, dining out<br>Savings (20%): KES 3,000 — emergency fund, future goals</p>
<h3>Tips for Students</h3>
<p>Start by tracking all expenses for one month. Use the Expense Tracker in this app to categorize every purchase. After 30 days, you'll have a clear picture of where your money goes, and you can adjust to meet the 50/30/20 targets.</p>""",
            category="Budgeting",
            read_time=4,
            icon="💰",
            difficulty="Beginner"
        ),
        Article(
            title="Building Your First Emergency Fund",
            summary="Why every student needs 3 months of expenses saved, and how to get there step by step.",
            content="""<h3>What is an Emergency Fund?</h3>
<p>An emergency fund is money set aside for unexpected expenses — a medical bill, a broken laptop, or sudden loss of income. It prevents you from going into debt when life surprises you.</p>
<h3>How Much Should You Save?</h3>
<p>Aim for <strong>3 months of living expenses</strong>. If you spend KES 12,000/month, your target is KES 36,000. This might sound daunting, but you can build it incrementally.</p>
<h3>Step-by-Step Plan</h3>
<ol>
<li><strong>Start small:</strong> Even KES 500/month builds a habit and fund over time</li>
<li><strong>Automate it:</strong> Treat savings like a bill — pay yourself first</li>
<li><strong>Keep it separate:</strong> Use a different account so you're not tempted to spend it</li>
<li><strong>Replenish if used:</strong> If you dip into it, make it a priority to rebuild</li>
</ol>
<h3>Where to Keep It</h3>
<p>A high-interest savings account or money market fund is ideal — your money earns interest while remaining accessible in an emergency. Avoid investing it in stocks since the value can fluctuate.</p>""",
            category="Savings",
            read_time=5,
            icon="🛡️",
            difficulty="Beginner"
        ),
        Article(
            title="Understanding Compound Interest",
            summary="The most powerful force in personal finance, explained with real numbers that will motivate you to start saving today.",
            content="""<h3>What is Compound Interest?</h3>
<p>Compound interest is earning interest on your interest. Over time, this creates exponential growth that Albert Einstein allegedly called "the eighth wonder of the world."</p>
<h3>A Simple Example</h3>
<p>Imagine you invest KES 10,000 at 10% annual interest:<br>
Year 1: KES 11,000<br>Year 2: KES 12,100<br>Year 5: KES 16,105<br>Year 10: KES 25,937<br>Year 20: KES 67,275</p>
<p>Without doing anything extra, your money grew 6.7x in 20 years!</p>
<h3>The Power of Starting Early</h3>
<p>Someone who starts saving at 20 vs 30 will have dramatically more wealth at retirement — even if the 30-year-old saves more money per month. Time is the most valuable ingredient.</p>
<h3>How to Use This</h3>
<p>Start investing small amounts now. Even KES 1,000/month starting at 20 can grow to over KES 3 million by age 60 at a 10% annual return. Use the Investment Simulator in this app to visualize your own projections.</p>""",
            category="Investing",
            read_time=6,
            icon="📈",
            difficulty="Beginner"
        ),
        Article(
            title="Student Loans: Borrowing Smart",
            summary="How to minimize debt, understand interest rates, and plan your repayment strategy before you graduate.",
            content="""<h3>Before You Borrow</h3>
<p>Exhaust all free money first — scholarships, grants, bursaries, work-study programs. Student loans should be your last resort, not your first option.</p>
<h3>Understanding Your Loan</h3>
<p>Key terms to know:<br>
<strong>Principal:</strong> The amount you borrowed<br>
<strong>Interest Rate:</strong> Annual cost of the loan (e.g., 12%)<br>
<strong>Capitalization:</strong> When unpaid interest is added to your principal<br>
<strong>Grace Period:</strong> Time after graduation before payments are due</p>
<h3>Strategies to Minimize Debt</h3>
<ul>
<li>Only borrow what you truly need — not the maximum offered</li>
<li>Pay interest while in school if possible — prevents capitalization</li>
<li>Work part-time to reduce reliance on loans</li>
<li>Graduate on time — extra semesters multiply your debt</li>
</ul>
<h3>Repayment Planning</h3>
<p>Create a loan repayment plan before you graduate. Know your monthly payment, total interest cost, and payoff date. The Savings Goals feature can help you plan ahead.</p>""",
            category="Debt",
            read_time=7,
            icon="🎓",
            difficulty="Intermediate"
        ),
        Article(
            title="Introduction to Investing for Students",
            summary="Stocks, bonds, index funds — a jargon-free beginner's guide to growing wealth while still in school.",
            content="""<h3>Why Invest as a Student?</h3>
<p>You have the most valuable asset: <strong>time</strong>. Even small investments now outperform larger investments later. The key is to start, not to start big.</p>
<h3>Investment Options</h3>
<p><strong>Savings Accounts / Money Market Funds</strong><br>Lowest risk, lower returns (5-10%). Good for emergency funds and short-term goals.</p>
<p><strong>Bonds / T-Bills</strong><br>Government-backed, medium returns (10-14% in Kenya). Stable and relatively safe.</p>
<p><strong>Index Funds / ETFs</strong><br>Diversified market exposure, historically ~10-12% annually. Ideal for long-term wealth building.</p>
<p><strong>Individual Stocks</strong><br>Higher potential, higher risk. Only invest money you can afford to lose.</p>
<h3>The Golden Rules</h3>
<ul>
<li>Never invest money you'll need in the next 2-3 years</li>
<li>Diversify — don't put all eggs in one basket</li>
<li>Invest regularly (monthly) regardless of market conditions</li>
<li>Ignore short-term market noise — focus on long-term goals</li>
</ul>""",
            category="Investing",
            read_time=8,
            icon="🚀",
            difficulty="Intermediate"
        ),
        Article(
            title="Side Hustles for Students in Kenya",
            summary="Practical ways to earn extra income while studying, from freelancing to campus business ideas.",
            content="""<h3>Digital Side Hustles</h3>
<p><strong>Freelancing:</strong> Offer skills on Upwork, Fiverr, or locally — writing, design, coding, video editing, tutoring. Even 5 hours/week can earn KES 5,000-20,000.</p>
<p><strong>Social Media Management:</strong> Many small businesses need help. Charge KES 5,000-15,000/month per client.</p>
<p><strong>Online Tutoring:</strong> Teach subjects you excel at via platforms like Preply or locally via WhatsApp groups.</p>
<h3>Campus Business Ideas</h3>
<ul>
<li>Sell food/snacks in the hostel</li>
<li>Printing and binding services</li>
<li>Laundry services for fellow students</li>
<li>Photography for events</li>
<li>Delivery/errand running</li>
</ul>
<h3>Managing Income</h3>
<p>When you earn extra money, follow a strict split: 50% to savings/goals, 30% for expenses, 20% for yourself. Don't let lifestyle inflation eat your earnings. Use the Budget Planner to track your hustle income separately.</p>""",
            category="Income",
            read_time=5,
            icon="💼",
            difficulty="Beginner"
        ),
    ]

    for article in articles:
        db.session.add(article)
    db.session.commit()

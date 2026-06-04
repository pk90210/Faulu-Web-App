from flask import Blueprint, render_template, request
from models.education import Article

education_bp = Blueprint('education', __name__)

@education_bp.route('/education')
def index():
    category_filter = request.args.get('category', '')
    if category_filter:
        articles = Article.query.filter_by(category=category_filter).all()
    else:
        articles = Article.query.all()
    categories = db_categories()
    return render_template('education/index.html',
        articles=articles,
        categories=categories,
        active_category=category_filter
    )

@education_bp.route('/education/<int:article_id>')
def article(article_id):
    art = Article.query.get_or_404(article_id)
    related = Article.query.filter_by(category=art.category).filter(Article.id != art.id).limit(3).all()
    return render_template('education/article.html', article=art, related=related)

def db_categories():
    from extensions import db
    from sqlalchemy import distinct
    result = db.session.query(distinct(Article.category)).all()
    return [r[0] for r in result]

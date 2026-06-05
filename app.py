from flask import Flask
from config import Config
from extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.budget import budget_bp
    from routes.savings import savings_bp
    from routes.expenses import expenses_bp
    from routes.education import education_bp
    from routes.simulator import simulator_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(savings_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(education_bp)
    app.register_blueprint(simulator_bp)

    with app.app_context():
        db.create_all()
        from models.education import seed_articles  
        seed_articles()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
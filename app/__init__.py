
from flask import Flask, request
import os

from flask_login import LoginManager, current_user
from datetime import datetime
from app.extensions import db
from app.models import User
from app.filters import register_filters 


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')

    # Register blueprints
    from app.routes.admin import admin_bp
    from app.routes.home import home_bp
    from app.routes.auth import auth_bp
    from app.routes.ai import ai_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ai_bp)

    # Initialize extensions
    login_manager = LoginManager()
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from flask_migrate import Migrate
    migrate = Migrate()
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    register_filters(app)

    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    @app.context_processor
    def inject_home_button_flag():
        return {
            'show_home_button': (
                current_user.is_authenticated and
                current_user.role != 'admin' and
                request.endpoint != 'home.home'
            )
        }

    return app







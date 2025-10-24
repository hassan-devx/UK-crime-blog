import os
from flask import Flask, request
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from datetime import datetime

from app.extensions import db
from app.models import User
from app.filters import register_filters

# Optional: import your config class
from config import Config  # Make sure config.py exists and defines Config


from app.models import User  # ✅ Must be imported before migrate.init_app

from dotenv import load_dotenv

import nltk


def create_app():
    load_dotenv() # Load environment variables from .env file
    app = Flask(__name__)
    app.config['DEBUG'] = True 

    
    nltk.download('vader_lexicon')

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from app.routes.admin import admin_bp
    from app.routes.home import home_bp
    from app.routes.auth import auth_bp
    from app.routes.ai import ai_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ai_bp)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register custom Jinja filters
    register_filters(app)

    # Track user activity
    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    # Inject UI flags into templates
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


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user  # ✅ current_user added
import markdown
import bleach

from app.extensions import db

from datetime import datetime, timezone





def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database.db'


    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from app.routes.home import home_bp
    from app.routes.auth import auth_bp  # ✅ move this import here

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)     # ✅ move this line inside the function
    
    

    login_manager = LoginManager()
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

   

    from flask_migrate import Migrate

    migrate = Migrate()
    migrate.init_app(app, db)
    

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    register_filters(app)

    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    return app
   

    


def markdown_filter(text):
    html = markdown.markdown(text)
    return bleach.clean(html)

# Register the filter globally
def register_filters(app):
    app.jinja_env.filters['markdown'] = markdown_filter




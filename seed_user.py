from app import create_app, db
from app.models import User, Role
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()
with app.app_context():
    existing = User.query.filter_by(email='hakinleye1@gmail.com').first()
    if existing:
        print("⚠️ User already exists. Skipping insert.")
    else:
        role = Role.query.filter_by(name='Admin').first()
        if not role:
            print("❌ Admin role not found. Please seed roles first.")
        else:
            user = User(
                username='Hassan',
                email='hakinleye1@gmail.com',
                password_hash=generate_password_hash('securepassword'),
                role=role,
                region='South Wales',
                last_seen=datetime.utcnow()
            )
            db.session.add(user)
            db.session.commit()
            print("✅ Admin user seeded.")
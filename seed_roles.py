from app import create_app, db
from app.models import Role

app = create_app()
with app.app_context():
    roles = ['Admin', 'Editor', 'Viewer']
    for name in roles:
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name))
            print(f"✅ Added role: {name}")
        else:
            print(f"⚠️ Role already exists: {name}")
    db.session.commit()
    print("🎉 Role seeding complete.")
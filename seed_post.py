from app import create_app, db
from app.models import Post, User
from datetime import datetime, timezone

app = create_app()
with app.app_context():
    author = User.query.filter_by(username='Hassan').first()
    if not author:
        print("❌ No user found with username 'hassan'. Please seed a user first.")
    else:
        title = "Crime Hotspots in South Wales"
        existing = Post.query.filter_by(title=title).first()

        if not existing:
            post = Post(
                title=title,
                content="<p>This heatmap reveals the most concentrated areas of crime across South Wales from 2022 to 2025.</p>",
                likes=15,
                views=120,
                timestamp=datetime.now(timezone.utc),

                author=author  # ✅ This sets author_id correctly
            )
            db.session.add(post)
            db.session.commit()
            print("✅ Post added successfully!")
        else:
            print("⚠️ Post already exists. Skipping insert.")
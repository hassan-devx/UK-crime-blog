from app import create_app, db
from app.models import Post

app = create_app()
with app.app_context():
    title = "Crime Hotspots in South Wales"
    existing = Post.query.filter_by(title=title).first()

    if not existing:
        post = Post(
            title=title,
            content="<p>This heatmap reveals the most concentrated areas of crime across South Wales from 2022 to 2025.</p>",
            likes=15,
            views=120
        )
        db.session.add(post)
        db.session.commit()
        print("✅ Post added successfully!")
    else:
        print("⚠️ Post already exists. Skipping insert.")
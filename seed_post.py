from app import app, db
from app.models import Post

with app.app_context():
    post = Post(
        title="Crime Hotspots in South Wales",
        content="<p>This heatmap reveals the most concentrated areas of crime across South Wales from 2022 to 2025.</p>",
        likes=15,
        views=120
    )
    db.session.add(post)
    db.session.commit()
    print("✅ Post added successfully!")
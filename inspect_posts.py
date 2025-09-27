from app import app
from app.models import Post

with app.app_context():
    posts = Post.query.all()
    for post in posts:
        print(f"ID: {post.id}, Title: {post.title}, Views: {post.views}, Likes: {post.likes}")
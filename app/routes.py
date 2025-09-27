from flask import render_template
from app import app
from app.models import Post

@app.route('/')
def home():
    return "Homepage is working!"

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


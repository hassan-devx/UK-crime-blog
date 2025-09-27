from flask import render_template, redirect, url_for, flash
from app import app, db
from app.models import Post
from app.forms import PostForm

@app.route('/')
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)



@app.route('/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            likes=0,
            views=0
        )
        db.session.add(post)
        db.session.commit()
        flash('Post published!', 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', form=form)


@app.route('/dashboard')
def dashboard():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('dashboard.html', posts=posts)


from app.forms import CommentForm
from app.models import Comment

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            author=form.author.data,
            content=form.content.data,
            post=post
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!', 'success')
        return redirect(url_for('show_post', post_id=post.id))
    return render_template('post.html', post=post, form=form)


@app.route('/heatmap')
def heatmap():
    return render_template('heatmap.html')
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
home_bp = Blueprint('home', __name__)
from sqlalchemy import func
from app.models import Post, Comment

from app import db
from app.models import Post
from app.forms import PostForm
from flask import request
from flask_login import login_required
from app.models import Reaction, Comment

from flask_login import current_user

from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image


from markupsafe import Markup
import markdown

from app.routes.ai import analyze_sentiment
from app.routes.ai import summarize_post

@home_bp.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.views += 1
    db.session.commit()

    comments = Comment.query.filter_by(post_id=post.id).all()
    rendered_content = Markup(markdown.markdown(post.content))
    return render_template('post.html', post=post, comments=comments, rendered_content=rendered_content)



from PIL import Image
from werkzeug.utils import secure_filename
import os

@home_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if current_user.role != 'admin':
        abort(403)  # Forbidden

    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        summary = summarize_post(content)  # ✅ AI summary added
        thumbnail_file = form.thumbnail.data
        plot_html = None

        filename = None
        if thumbnail_file and thumbnail_file.filename != '':
            filename = secure_filename(thumbnail_file.filename)
            thumbnail_path = os.path.join(current_app.root_path, 'static', 'thumbnails', filename)
            thumbnail_file.save(thumbnail_path)

            try:
                img = Image.open(thumbnail_path)
                img.verify()
                img = Image.open(thumbnail_path)
                img = img.convert('RGB')
                img.thumbnail((600, 400))
                img.save(thumbnail_path)
            except Exception as e:
                os.remove(thumbnail_path)
                flash('Invalid image file. Please upload a valid image.', 'danger')
                return redirect(url_for('home.new_post'))

        post = Post(
            title=title,
            content=content,
            summary=summary,  # ✅ Save summary
            author=current_user,
            thumbnail=filename,
            plot_html=plot_html
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home.home'))

    return render_template('new_post.html', form=form)



#@home_bp.route('/dashboard')
#def dashboard():
 #   posts = Post.query.order_by(Post.timestamp.desc()).all()
  #  return render_template('dashboard.html', posts=posts)


from app.forms import CommentForm
from app.models import Comment

@home_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('home.show_post', post_id=post.id))
    return render_template('post.html', post=post, form=form)


@home_bp.route('/heatmap')
def render_heatmap():
    return render_template('heatmap.html')


@home_bp.route('/heatmap')
def heatmap():
    crime_type = request.args.get('crime_type')
    year = request.args.get('year')

    df = pd.read_csv('filtered_crime_data.csv')

    if crime_type:
        df = df[df['Crime Type'] == crime_type]
    if year:
        df = df[df['Year'] == int(year)]

    m = folium.Map(location=[51.6214, -3.9436], zoom_start=12)
    heat_data = df[['Latitude', 'Longitude']].dropna().values.tolist()
    HeatMap(heat_data).add_to(m)

    m.save('app/templates/heatmap.html')
    return render_template('heatmap.html')

import pandas as pd
from app.models import Post, Comment
from sqlalchemy import func

@home_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        abort(403)

            # Load data
    df = pd.read_csv(r"C:\Users\User\Desktop\UK-crime-blog\filtered_crime_data.csv")
    df['Crime type'] = df['Crime type'].str.strip()
    df['City'] = df['LSOA name'].str.extract(r'^([A-Za-z\s]+)\s')
    df['Month'] = df['Month'].str.strip()

    # Extract unique values for dropdowns
    crime_types = sorted(df['Crime type'].unique())
    regions = sorted(df['City'].dropna().unique())


    years = sorted(df['Month'].str[:4].unique())


    print("Extracted cities:", df['City'].unique())
    # Apply filters
    crime_type = request.args.get('crime_type')
    year = request.args.get('year')
    region = request.args.get('region')


    if crime_type:
        df = df[df['Crime type'] == crime_type]
    if year:
        df = df[df['Month'].str[:4] == year]
    if region:
        df = df[df['City'] == region]

    # Stats
    total_crimes = len(df)
    crime_counts = {k: int(v) for k, v in df['Crime type'].value_counts().to_dict().items()}
    df['Year'] = df['Month'].str[:4].astype(int)
    year_counts = {int(k): int(v) for k, v in df['Year'].value_counts().sort_index().to_dict().items()}

    # Posts
    posts = db.session.query(
        Post,
        func.count(Comment.id).label('comment_count')
    ).outerjoin(Comment).group_by(Post.id).order_by(Post.timestamp.desc()).all()

    return render_template('admin/dashboard.html',
                        posts=posts,
                        total_crimes=total_crimes,
                        crime_counts=crime_counts,
                        year_counts=year_counts,
                        selected_type=crime_type,
                        selected_year=year,
                        selected_region=region,
                        crime_types=crime_types,
                        regions=regions,
                        years=years)




@home_bp.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.likes += 1
    db.session.commit()
    return redirect(url_for('home.show_post', post_id=post.id))

from flask_login import current_user

from flask_login import current_user

import markdown
import bleach



@home_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form['content']

    new_comment = Comment(
        content=content,
        post_id=post.id,
        author_id=current_user.id  # ✅ This links the comment to the logged-in user
    )

    db.session.add(new_comment)
    db.session.commit()
    flash('Comment added!', 'success')
    return redirect(url_for('home.show_post', post_id=post.id))



from bs4 import BeautifulSoup

@home_bp.route('/edit_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        raw_content = request.form['content']
        safe_html = bleach.clean(markdown.markdown(raw_content))
        comment.content = safe_html
        db.session.commit()
        flash("Comment updated.")
        return redirect(url_for('home.show_post', post_id=comment.post_id))

    # ✅ Strip HTML tags for editing
    from bs4 import BeautifulSoup

    raw_text = BeautifulSoup(comment.content, "html.parser").get_text()
    return render_template('home/edit_comment.html', raw_text=raw_text, comment=comment)


@home_bp.route('/react/<int:comment_id>/<emoji>', methods=['POST'])
@login_required
def react_to_comment(comment_id, emoji):
    comment = Comment.query.get_or_404(comment_id)
    reaction = Reaction.query.filter_by(user_id=current_user.id, comment_id=comment_id, emoji=emoji).first()

    if not reaction:
        new_reaction = Reaction(user_id=current_user.id, comment_id=comment_id, emoji=emoji)
        db.session.add(new_reaction)
    else:
        db.session.delete(reaction)  # toggle off

    db.session.commit()
    return redirect(request.referrer)



@home_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('home.show_post', post_id=post.id))

    return render_template('edit_post.html', post=post)


@home_bp.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'info')
    return redirect(url_for('home.dashboard'))


@home_bp.route('/react', methods=['POST'])
@login_required
def react():
    emoji = request.form.get('emoji')
    post_id = request.form.get('post_id')
    comment_id = request.form.get('comment_id')

    reaction = Reaction(
        emoji=emoji,
        user_id=current_user.id,
        post_id=post_id if post_id else None,
        comment_id=comment_id if comment_id else None
    )
    db.session.add(reaction)
    db.session.commit()
    return redirect(request.referrer)


@home_bp.route('/')
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    featured_posts = Post.query.order_by(Post.views.desc()).limit(3).all()
    return render_template('index.html', posts=posts, featured_posts=featured_posts)

@home_bp.route('/search')
def search():
    query = request.args.get('q', '')
    results = Post.query.filter(Post.title.ilike(f'%{query}%')).all()
    return render_template('search_results.html', query=query, results=results)



from app.routes.ai import analyze_sentiment  # make sure this is imported

@home_bp.route('/comment', methods=['POST'])
@login_required
def post_comment():
    comment_text = request.form['content']
    post_id = request.form['post_id']

    # 🔥 Analyze sentiment using your AI module
    sentiment = analyze_sentiment(comment_text)

    # 📝 Create and save the comment with sentiment
    new_comment = Comment(
        content=comment_text,
        sentiment=sentiment,
        user_id=current_user.id,
        post_id=post_id,
        timestamp=datetime.utcnow()
    )

    db.session.add(new_comment)
    db.session.commit()

    flash('Comment posted with sentiment: {}'.format(sentiment), 'success')
    return redirect(url_for('home.show_post', post_id=post_id))

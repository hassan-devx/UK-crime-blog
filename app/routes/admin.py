from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from datetime import datetime

from sqlalchemy import func
from app.models import Post, Comment
from app import db

from app.utils.decorators import admin_required

from collections import Counter
from app.models import Reaction, Comment, Post

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    crime_counts = {
        'Burglary': 42,
        'Robbery': 17,
        'Assault': 33,
        'Vandalism': 21
    }

    year_counts = {
        2020: 120,
        2021: 145,
        2022: 132,
        2023: 158,
        2024: 166
    }

    return render_template('admin/dashboard.html', crime_counts=crime_counts, year_counts=year_counts)



@admin_bp.route('/')
@admin_required
def admin_panel():
    import pandas as pd
    from app.models import Post, Comment, User

    # Load crime data
    try:
        df = pd.read_csv(r"C:\Users\User\Desktop\UK-crime-blog\filtered_crime_data.csv")
        total_crimes = len(df)
        recent_crimes = df['Crime type'].value_counts().head(5).to_dict()
    except Exception as e:
        total_crimes = 0
        recent_crimes = {}
        print(f"Error loading crime data: {e}")

    # Fetch posts with comment counts
    posts = db.session.query(
        Post,
        func.count(Comment.id).label('comment_count')
    ).outerjoin(Comment).group_by(Post.id).order_by(Post.timestamp.desc()).all()

    # Fetch recent comments
    comments = Comment.query.order_by(Comment.timestamp.desc()).limit(10).all()

    # Fetch all users for leaderboard or moderation
    users = User.query.all()

    # Current year for footer
    current_year = datetime.utcnow().year

    return render_template('admin.html',
                           posts=posts,
                           comments=comments,
                           users=users,
                           total_crimes=total_crimes,
                           recent_crimes=recent_crimes,
                           current_year=current_year)




@admin_bp.route('/user-analytics', endpoint='user_analytics')
@admin_required
def user_analytics():
   
 

    # Get current user's reactions
    reaction_counts = db.session.query(
        Reaction.emoji,
        func.count(Reaction.id)
    ).filter_by(user_id=current_user.id).group_by(Reaction.emoji).all()

    emoji_totals = {emoji: count for emoji, count in reaction_counts}

    comment_count = Comment.query.filter_by(author_id=current_user.id).count()
    post_count = Post.query.filter_by(author_id=current_user.id).count()
   
    comments = Comment.query.filter_by(author_id=current_user.id).all()

    return render_template('admin/user_analytics.html',
                           emoji_totals=emoji_totals,
                           comment_count=comment_count,
                           post_count=post_count)




@admin_bp.route('/emoji-chart')
@login_required
def emoji_chart():
    from app.models import Reaction
    from sqlalchemy import func

    emoji_counts = db.session.query(
        Reaction.emoji,
        func.count(Reaction.id)
    ).group_by(Reaction.emoji).all()

    labels = [emoji for emoji, _ in emoji_counts]
    data = [count for _, count in emoji_counts]

    return render_template('emoji_chart.html', labels=labels, data=data)



@admin_bp.route('/leaderboard')

def leaderboard():
    from app.models import User, Post, Comment
    from sqlalchemy import func

    leaderboard = db.session.query(
        User.username,
        func.count(Post.id).label('post_count'),
        func.count(Comment.id).label('comment_count')
    ).select_from(User) \
     .outerjoin(Post, Post.author_id == User.id) \
     .outerjoin(Comment, Comment.author_id == User.id) \
     .group_by(User.id) \
     .order_by(func.count(Post.id).desc()) \
     .all()

    return render_template('leaderboard.html', leaderboard=leaderboard)


@admin_bp.route('/inactive-users')
@login_required
def inactive_users():
    from app.models import User
    from datetime import datetime, timedelta

    threshold = datetime.utcnow() - timedelta(days=30)
    inactive = User.query.filter(User.last_seen < threshold).all()

    return render_template('inactive_users.html', inactive=inactive)







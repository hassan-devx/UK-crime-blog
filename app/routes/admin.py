from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user


from sqlalchemy import func
from app.models import Post, Comment
from app import db

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')






@admin_bp.route('/')
@login_required
def admin_panel():
    if current_user.username != 'Hassan':
        abort(403)

    from app.models import Post, Comment
    import pandas as pd

    posts = db.session.query(
    Post,
    func.count(Comment.id).label('comment_count')
    ).outerjoin(Comment).group_by(Post.id).order_by(Post.timestamp.desc()).all()

    comments = Comment.query.order_by(Comment.timestamp.desc()).all()

    df = pd.read_csv(r"C:\Users\User\Desktop\UK-crime-blog\filtered_crime_data.csv")
    total_crimes = len(df)
    recent_crimes = df['Crime type'].value_counts().head(5).to_dict()

    return render_template('admin.html',
                           posts=posts,
                           comments=comments,
                           total_crimes=total_crimes,
                           recent_crimes=recent_crimes)



@admin_bp.route('/user-analytics')
@login_required
def user_analytics():
    from collections import Counter
    from app.models import Reaction, Comment, Post

    # Get current user's reactions
    reaction_counts = db.session.query(
        Reaction.emoji,
        func.count(Reaction.id)
    ).filter_by(user_id=current_user.id).group_by(Reaction.emoji).all()

    emoji_totals = {emoji: count for emoji, count in reaction_counts}

    comment_count = Comment.query.filter_by(author_id=current_user.id).count()
    post_count = Post.query.filter_by(author_id=current_user.id).count()
   
    comments = Comment.query.filter_by(author_id=current_user.id).all()

    return render_template('user_analytics.html',
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
@login_required
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
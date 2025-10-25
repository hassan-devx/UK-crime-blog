from datetime import datetime, timezone
from app import db
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    likes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)

    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='posts')
    thumbnail = db.Column(db.String(120), nullable=True)
    plot_html = db.Column(db.Text, nullable=True)



from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(10))  # 'positive', 'neutral', 'negative'

    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', back_populates='comments')

    reactions = db.relationship('Reaction', backref='comment', lazy='dynamic')
    



    def sentiment(self):
        sia = SentimentIntensityAnalyzer()
        score = sia.polarity_scores(self.content)['compound']
        return 'Positive' if score > 0.05 else 'Negative' if score < -0.05 else 'Neutral'


from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', back_populates='users')

    region = db.Column(db.String(100), default="South Wales")
    comments = db.relationship('Comment', back_populates='author')
    reactions = db.relationship('Reaction', backref='user')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emoji = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_reaction_user'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', name='fk_reaction_post'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id', name='fk_reaction_comment'), nullable=True)

   
    post = db.relationship('Post', backref='reactions')
  

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    users = db.relationship('User', back_populates='role')

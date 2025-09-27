from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Publish')


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired()])
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')
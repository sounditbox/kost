from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    content = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Создать пост')

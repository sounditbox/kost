from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.fields import StringField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired


class NewArticleForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    image = FileField('Изображение', validators=[DataRequired()])
    content = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Создать пост')

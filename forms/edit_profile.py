from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField


class EditProfileForm(FlaskForm):
    name = StringField('Имя')
    about = StringField('О себе')
    image = FileField('Выберите файл:')
    submit = SubmitField('Сохранить изменения')

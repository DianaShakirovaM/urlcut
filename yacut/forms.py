from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class UrlForm(FlaskForm):
    original_link = URLField(
        'Оригинальная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 255)]
    )
    custom_id = URLField(
        'Короткая ссылка',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Добавить')


class FileForm(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField('Загрузить')

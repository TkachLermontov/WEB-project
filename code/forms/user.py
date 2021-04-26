from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя клиента', validators=[DataRequired()])
    number = StringField('Номер клиента', validators=[DataRequired()])
    about = TextAreaField("Немного о стрижке")
    date = DateField('Дата')
    submit = SubmitField('Записаться')

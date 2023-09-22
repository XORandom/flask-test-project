from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError  # Поле заполнено, формат ввода

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Логин:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(),
                                          EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Регистрация')


    def validate_username(self, username):
        """
        Проверяет, не занято ли имя пользователя.

        :param username:
        :return:
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Имя пользователя занято!')


    def validate_email(self, email):
        """
        Проверяет, не зарегистрирован ли email

        :param email:
        :param username:
        :return:
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('На эту почту уже зарегистрирован аккаунт')

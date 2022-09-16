from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, ValidationError
from wb.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', )
    confirmpassword = PasswordField('Repeat Password', [DataRequired(), EqualTo('password'), Length(min=3)])

    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken!')


class LoginForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Nombre or correo')
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=3)])
    rememberme = BooleanField('Recuérdame')
    submit = SubmitField('Entrar')




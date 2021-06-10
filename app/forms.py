from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.validators import DataRequired,Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sing In')
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
class predlogForm(FlaskForm):
    FirstName = StringField('FirstName', validators=[DataRequired()])
    LastName = StringField('LastName',validators=[DataRequired()])
    Offer = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Registrate')
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    FirstName = StringField('FistName')
    SecondName = StringField('SecondName')
    age = StringField('age')
    language =StringField('gender')
    city = StringField('city')
    work = StringField('work')
    Music = StringField('Music')
    about_me = TextAreaField('about me')
    submit = SubmitField('submit')
class PostForm(FlaskForm):
    post = TextAreaField('Post')
    submit = SubmitField('submit')
class vipForm(FlaskForm):
    username = StringField('User Name')
    viplvl = StringField('Vip lvl')
    submit = SubmitField('Submit')
class deleteForm(FlaskForm):
    submit = SubmitField('delete')
class commentsForm(FlaskForm):
    username = StringField('username')
    comments= TextAreaField('Comment')
    addcomment = SubmitField('submit')
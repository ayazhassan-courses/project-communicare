from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
     validators=[DataRequired(),Length(min=2, max=20)])

    email = StringField('Email',
    validators=[DataRequired(), Email()])

    password = PasswordField('Password',
    validators=[DataRequired()])

    confirm_password = PasswordField('Comfirm Password',
    validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('Username Taken')

    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('Email Taken')

class LoginForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(), Email()])

    password = PasswordField('Password',validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    location = HiddenField("Location", id="hidden_field")

    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
     validators=[DataRequired(),Length(min=2, max=20)])

    email = StringField('Email',
    validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username= username.data).first()
            if user:
                raise ValidationError('Username Taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email= email.data).first()
            if user:
                raise ValidationError('Email Taken')


class PostForm(FlaskForm):
    title = StringField('What do you want to ask for/ giveaway?', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    phone_no = StringField('Enter your Number', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post')
    location2 = HiddenField("Location", id="hidden_field2")


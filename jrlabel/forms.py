from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , BooleanField , FileField ,TextAreaField
from wtforms.validators import DataRequired , Length , Email , EqualTo , ValidationError
from jrlabel.models import User
from flask_wtf.file import FileAllowed
from flask_login import   current_user 




class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class ArticleForm1(FlaskForm):
    img_file = FileField('Update Image', validators=[DataRequired() ,FileAllowed(['jpg', 'png'])])
    p_text = StringField('Paragraph Text', validators=[DataRequired()])
    h2_text = StringField('Header Text', validators=[DataRequired()])
    submit = SubmitField('Update')



class ArticleForm2(FlaskForm):
    img_file = FileField('Update Image', validators=[DataRequired() ,FileAllowed(['jpg', 'png'])])
    p_text = StringField('Paragraph Text', validators=[DataRequired()])
    h2_text = StringField('Header Text', validators=[DataRequired()])
    submit = SubmitField('Update')



class ArticleForm3(FlaskForm):
    img_file = FileField('Update Image', validators=[DataRequired() ,FileAllowed(['jpg', 'png'])])
    p_text = StringField('Paragraph Text', validators=[DataRequired()])
    h2_text = StringField('Header Text', validators=[DataRequired()])
    submit = SubmitField('Update')



class ArticleForm4(FlaskForm):
    img_file = FileField('Update Image', validators=[DataRequired() ,FileAllowed(['jpg', 'png'])])
    p_text = StringField('Paragraph Text', validators=[DataRequired()])
    h2_text = StringField('Header Text', validators=[DataRequired()])
    submit = SubmitField('Update')


class ArticleForm5(FlaskForm):
    img_file = FileField('Update Image', validators=[DataRequired() ,FileAllowed(['jpg', 'png'])])
    p_text = StringField('Paragraph Text', validators=[DataRequired()])
    h2_text = StringField('Header Text', validators=[DataRequired()])
    submit = SubmitField('Update')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

        





class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image_file = FileField('Update Image', validators=[DataRequired(), FileAllowed(['jpg', 'png','jpeg'])])

    submit = SubmitField('Post')
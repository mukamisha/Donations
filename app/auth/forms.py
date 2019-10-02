from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField, TextAreaField, RadioField
from wtforms.validators import Required,Email,EqualTo
from ..models import User
from wtforms import ValidationError


class RegistrationForm(FlaskForm):

    email = StringField('Your Email Address',validators=[Required(),Email()])
    username = StringField('Enter your username',validators = [Required()])
    password = PasswordField('Password',validators = [Required(),
    EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
            if User.query.filter_by(email =data_field.data).first():
                raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')


class DonationForm(FlaskForm):
   name = StringField('names', validators=[Required()])
   email = StringField('Email',validators=[Required()])
   Phonenumber = StringField('Phonenumber',validators=[Required()])
   donation = TextAreaField("What are you donating?",validators=[Required()])
   category = RadioField('Label', choices=[ ('intertainment','intertainment'), ('politics','politics'),('health','health'),('education','education')],validators=[Required()])
   submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    password = PasswordField('Password',validators =[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')
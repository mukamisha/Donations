from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,RadioField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
	title = StringField('Title', validators=[Required()])
	description = TextAreaField("What would you like to pitch ?",validators=[Required()])
	category = RadioField('Label', choices=[ ('intertainment','intertainment'), ('politics','politics'),('health','health'),('education','education')],validators=[Required()])
	submit = SubmitField('Submit')

class DonationForm(FlaskForm):
    fullname = StringField('Fullnames', validators=[Required()])
    email = StringField('Email',validators=[Required()])
    Phonenumber = StringField('Phonenumber',validators=[Required()])
    category = RadioField('Label', choices=[ ('intertainment','intertainment'), ('politics','politics'),('health','health'),('education','education')],validators=[Required()])
    # category = RadioField('Label', choices=[ ('health','health'), ('education','education'),('disasters','disasters'),('justice','justice')],validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
	description = TextAreaField('Add comment',validators=[Required()])
	submit = SubmitField()

from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,RadioField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class DonationForm(FlaskForm):
	title = StringField('Title', validators=[Required()])
	description = TextAreaField("What would you like to donate ?",validators=[Required()])
	category = RadioField('Label', choices=[ ('health','health'), ('education','education'),('disasters','disasters'),('justice','justice')],validators=[Required()])
	submit = SubmitField('Submit')

class CommentForm(FlaskForm):
	description = TextAreaField('Add comment',validators=[Required()])
	submit = SubmitField()

class UpvoteForm(FlaskForm):
	submit = SubmitField()

class EventForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    description = TextAreaField("Post an Upcoming Event ?",validators=[Required()])
    category = RadioField('Label', choices=[ ('health','health'), (' education',' education'),('disasters','disasters'),('justice','justice')],validators=[Required()])
    submit = SubmitField('Submit')
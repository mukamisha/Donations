
from flask import render_template,request,redirect,url_for,abort
from . import main
# from ..request import get_movies,get_movie,search_movie
from .forms import PitchForm,CommentForm,UpdateProfile,DonationForm
from .. import db,photos
from ..models import User,Pitch,Comment,Upvote,Downvote,Donation,Subscription
from flask_login import login_required,current_user
import markdown2
 




# Views
@main.route('/', methods = ['GET','POST'])
def index():

   
    pitch = Pitch.query.filter_by().first()
    title = 'Home'
    intertainment = Pitch.query.filter_by(category="intertainment")
    politics = Pitch.query.filter_by(category = "politics")
    health = Pitch.query.filter_by(category = "health")
    education = Pitch.query.filter_by(category = "education")

    return render_template('index.html', title = title, pitch = pitch, intertainment=intertainment, politics= politics, health = health, education = education)
    

@main.route('/pitches/new/', methods = ['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()
    subscribe = Subscription.query.all()
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        user_id = current_user
        category = form.category.data
        print(current_user._get_current_object().id)
        new_pitch = Pitch(user_id =current_user._get_current_object().id, title = title,description=description,category=category)
        db.session.add(new_pitch)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('pitch.html',form=form)



@main.route('/comment/new/<int:pitch_id>', methods = ['GET','POST'])
@login_required
def new_comment(pitch_id):
    form = CommentForm()
    
    pitch=Pitch.query.get(pitch_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id, pitch_id = pitch_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', pitch_id= pitch_id))

    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    return render_template('comment.html', form = form, comment = all_comments, pitch = pitch )

@main.route('/donate/new/<int:pitch_id>', methods = ['GET','POST'])
@login_required
def new_donation(pitch_id):
    form = DonationForm()
    subscribe = Subscription.query.all()
    pitch=Pitch.query.get(pitch_id)
    if form.validate_on_submit():
        fullname = form.fullname.data
        email = form.email.data
        Phonenumber = form.Phonenumber.data
        new_donation = Donation(fullname = fullname, email = email, Phonenumber = Phonenumber, user_id = current_user._get_current_object().id, pitch_id = pitch_id)
        db.session.add(new_donation)
        db.session.commit()

        for email in subscribe:
            mail_message("New Blog Alert!!!!",
                         "email/blog_alert", email.email, subscribe=subscribe)

        return redirect(url_for('.new_donation', pitch_id= pitch_id))

    all_donations = Donation.query.filter_by(pitch_id = pitch_id).all()
    return render_template('donation.html', form = form, donation = all_donations, pitch = pitch )

@main.route('/pitch/upvote/<int:pitch_id>/upvote', methods = ['GET', 'POST'])
@login_required
def upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes = Upvote.query.filter_by(pitch_id= pitch_id)
    
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))


    new_upvote = Upvote(pitch_id=pitch_id, user = current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))


@main.route('/pitch/downvote/<int:pitch_id>/downvote', methods = ['GET', 'POST'])
@login_required
def downvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_downvotes = Downvote.query.filter_by(pitch_id= pitch_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.pitch_id==pitch_id).first():
        return  redirect(url_for('main.index'))


    new_downvote = Downvote(pitch_id=pitch_id, user = current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))

@main.route('/user/<uname>')
@login_required
def profile(uname):
 user = User.query.filter_by(username = uname).first()
 get_pitches = Pitch.query.filter_by(user_id = current_user.id).all()
 if user is None:
     abort(404)
 return render_template("profile/profile.html", user = user, pitches_content = get_pitches)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))



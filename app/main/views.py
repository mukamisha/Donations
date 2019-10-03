
from flask import render_template,request,redirect,url_for,abort
from . import main
# from ..request import get_movies,get_movie,search_movie
from .forms import DonationForm,CommentForm,UpvoteForm,UpdateProfile, EventForm
from .. import db,photos
from ..models import User,Donation,Comment,Upvote,Subscription, Event
from flask_login import login_required,current_user
import markdown2
 




# Views
@main.route('/', methods = ['GET','POST'])
def index():
#    event = Event.query.filter_by().first()
#    title = 'EVENT'
#    health = Event.query.filter_by(category="health")
#    education = Event.query.filter_by(category = "education")
#    disasters = Event.query.filter_by(category = "disasters")
#    justice = Event.query.filter_by(category = "justice")
   return render_template('index.html')


@main.route('/home', methods = ['GET','POST'])
def home():
   event = Event.query.filter_by().first()
   title = 'EVENT'
   health = Event.query.filter_by(category="health")
   education = Event.query.filter_by(category = "education")
   disasters = Event.query.filter_by(category = "disasters")
   justice = Event.query.filter_by(category = "justice")
   return render_template('home.html', title = title, event = event, health=health, education= education, disasters = disasters,justice = justice)


@main.route('/donation/new/', methods = ['GET','POST'])
@login_required
def new_donation():
    form = DonationForm()
    subscribe = Subscription.query.all()
    if form.validate_on_submit():

        description = form.description.data
        title = form.title.data
        user_id = current_user
        category = form.category.data
        print(current_user._get_current_object().id)
        new_donation = Donation(user_id =current_user._get_current_object().id, title = title,description=description,category=category)
        db.session.add(new_donation)
        db.session.commit()

        for email in subscribe:
           mail_message("New Blog Alert!!!!",
                        "email/blog_alert", email.email, subscribe=subscribe)
        return redirect(url_for('.new_donation', donation_id=donation_id))
        all_donations = Donation.query.filter_by(donation_id = donation_id).all()
    return render_template('donation.html',form=form, donation = all_donations)



@main.route('/comment/new/<int:event_id>', methods = ['GET','POST'])
@login_required
def new_comment(event_id):
    form = CommentForm()
    event=Event.query.get(event_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id, event_id = event_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.home', event_id= event_id))

    all_comments = Comment.query.filter_by(event_id = event_id).all()
    return render_template('comment.html', form = form, comment = all_comments, event = event )

@main.route('/event/upvote/<int:event_id>/upvote', methods = ['GET', 'POST'])
@login_required
def upvote(event_id):
    event = Event.query.get(event_id)
    user = current_user
    event_upvotes = Upvote.query.filter_by(event_id= event_id)
    
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.event_id==event_id).first():
        return  redirect(url_for('main.home'))


    new_upvote = Upvote(event_id=event_id, user = current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.home'))


@main.route('/user/<uname>')
@login_required
def profile(uname):
 user = User.query.filter_by(username = uname).first()
 get_donations = Donation.query.filter_by(user_id = current_user.id).all()
 if user is None:
     abort(404)
 return render_template("profile/profile.html", user = user, donationS_content = get_donations)

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



@main.route('/events/new/', methods = ['GET','POST'])
@login_required
def new_event():
   form = EventForm()
   if form.validate_on_submit():
       description = form.description.data
       title = form.title.data
       user_id = current_user
       category = form.category.data
       print(current_user._get_current_object().id)
       new_event = Event(user_id =current_user._get_current_object().id, title = title,description=description,category=category)
       db.session.add(new_event)
       db.session.commit()
       return redirect(url_for('main.home'))
   return render_template('event.html',form=form)



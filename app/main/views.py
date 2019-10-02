
from flask import render_template,request,redirect,url_for,abort
from . import main
# from ..request import get_movies,get_movie,search_movie
from .forms import EventForm,CommentForm,LikeForm
from .. import db,photos
from ..models import User,Event,Comment,Like
from flask_login import login_required,current_user
import markdown2
 

# Views
@main.route('/', methods = ['GET','POST'])
def index():


    event = Event.query.filter_by().first()
    title = 'EVENT'
    health = Event.query.filter_by(category="health")
    education = Event.query.filter_by(category = "education")
    disasters = Event.query.filter_by(category = "disasters")
    justice = Event.query.filter_by(category = "justice")

    return render_template('index.html', title = title, event = event, health=health, education= education, disasters = disasters,justice = justice)
    

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
        return redirect(url_for('main.index'))
    return render_template('event.html',form=form)



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


        return redirect(url_for('.new_comment', event_id= event_id))

    all_comments = Comment.query.filter_by(event_id = event_id).all()
    return render_template('comment.html', form = form, comment = all_comments, event = event )

@main.route('/event/like/<int:event_id>/like', methods = ['GET', 'POST'])
@login_required
def like(event_id):
    event = Event.query.get(event_id)
    user = current_user
    event_likes = Like.query.filter_by(event_id= event_id)
    
    if Like.query.filter(Like.user_id==user.id,Like.event_id==event_id).first():
        return  redirect(url_for('main.index'))


    new_like = Like(event_id=event_id, user = current_user)
    new_like.save_likes ()
    return redirect(url_for('main.index'))






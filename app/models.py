from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
# from datetime import datetime



    
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    donation = db.relationship('Donation', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref = 'user', lazy = 'dynamic')
    upvotes = db.relationship('Upvote', backref = 'user', lazy = 'dynamic')
    bio = db.Column(db.String(255))
    profile_pic_path =  db.Column(db.String(255))
    password_secure =  db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('Sorry You can not read the password')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    def __repr__(self):
        return f'User {self.username}'

class Donation(db.Model):
    '''
    a donation class
    '''
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    description = db.Column(db.String(), index = True)
    title = db.Column(db.String())
    category = db.Column(db.String(255), nullable=False)
    # comments = db.relationship('Comment',backref='donation',lazy='dynamic')
    # upvotes = db.relationship('Upvote', backref = 'donation', lazy = 'dynamic')

    
    @classmethod
    def get_donations(cls, id):
        donations = Donations.query.order_by(donations_id=id).desc().all()
        return donations

    def __repr__(self):
        return f'Donation {self.description}'

class Event(db.Model):
   __tablename__ = 'events'
   id = db.Column(db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
   description = db.Column(db.String(), index = True)
   title = db.Column(db.String())
   category = db.Column(db.String(255), nullable=False)
   comments = db.relationship('Comment',backref='event',lazy='dynamic')
   upvotes = db.relationship('Upvote', backref = 'event', lazy = 'dynamic')
   @classmethod
   def get_events(cls, id):
       events = Event.query.order_by(event_id=id).desc().all()
       return events
   def __repr__(self):
       return f'Event {self.description}'



class Comment(db.Model):
    __tablename__='comments'
    
    id = db.Column(db.Integer,primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    description = db.Column(db.Text)

    
    def __repr__(self):
        return f"Comment : id: {self.id} comment: {self.description}"




class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key=True)
    upvote = db.Column(db.Integer,default=1)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_upvotes(self):
        db.session.add(self)
        db.session.commit()


    def add_upvotes(cls,id):
        upvote_donation = Upvote(user = current_user, donation_id=id)
        upvote_donation.save_upvotes()

    
    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvote.query.filter_by(donation_id=id).all()
        return upvote

    @classmethod
    def get_all_upvotes(cls,donation_id):
        upvotes = Upvote.query.order_by('id').all()
        return upvotes

    def __repr__(self):
        return f'{self.user_id}:{self.donation_id}'

class Subscription(db.Model):
   __tablename__ = 'subscribers'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100))
   email = db.Column(db.String(100), unique=True)
   def __repr__(self):
       return f'User {self.name}'



        

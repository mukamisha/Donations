from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager




    
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    event = db.relationship('Event', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref = 'user', lazy = 'dynamic')
    likes = db.relationship('Like', backref = 'user', lazy = 'dynamic')
    bio = db.Column(db.String(255))
    profile_pic_path =  db.Column(db.String(255))
    # password_secure =  db.Column(db.String(255))

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

class Event(db.Model):
   
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    description = db.Column(db.String(), index = True)
    title = db.Column(db.String())
    category = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment',backref='event',lazy='dynamic')
    likes = db.relationship('Likes', backref = 'event', lazy = 'dynamic')
   

    
    @classmethod
    def get_events(cls, id):
        events = Event.query.order_by(pitch_id=id).desc().all()
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




class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer,primary_key=True)
    likes = db.Column(db.Integer,default=1)
    event_id = db.Column(db.Integer,db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_likes(self):
        db.session.add(self)
        db.session.commit()


    def add_likes(cls,id):
        like_event = Like(user = current_user, event_id=id)
        like_event.save_likes()

    
    @classmethod
    def get_likes(cls,id):
        like = Like.query.filter_by(event_id=id).all()
        return like

    @classmethod
    def get_all_likes(cls,event_id):
        likes = Like.query.order_by('id').all()
        return likes

    def __repr__(self):
        return f'{self.user_id}:{self.event_id}'



        

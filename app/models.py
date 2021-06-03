from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index =True, unique=True)
    email = db.Column(db.String(64), index=True,unique=True)
    password_hash=db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    vip = db.Column(db.Integer)
    aboutme = db.relationship('AboutMe',backref='User',uselist=False)
    
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    

    def __repr__(self):
       return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    author = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class predlog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    FirstName = db.Column(db.String(64))
    LastName = db.Column(db.String(64))
    Age = db.Column(db.Integer())
    offer = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Time = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<predlog {}>'.format(self.body)

class AboutMe(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    FirstName = db.Column(db.String(64))
    SecondName = db.Column(db.String(64))
    UserName = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    age = db.Column(db.Integer)
    city = db.Column(db.String(64))
    language = db.Column(db.String(64))
    Music = db.Column(db.String(64))
    Work = db.Column(db.String(64))
    about_me = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '< {}>'.format(self.body)
class DeletedPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delbody = db.Column(db.String(140))
    delauthor = db.Column(db.String(140))
    deltimestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
class DeleteUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    delusername = db.Column(db.String(64),index =True, unique=True)
    delemail = db.Column(db.String(64), index=True,unique=True)
    delpassword_hash=db.Column(db.String(128))
    delabout_me = db.Column(db.String(140))
    dellast_seen = db.Column(db.DateTime, default=datetime.utcnow)
    delvip = db.Column(db.Integer)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
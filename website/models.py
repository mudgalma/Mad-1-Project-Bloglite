from.import db
from sqlalchemy.sql import func
from flask_login import UserMixin
Followers=db.Table('Followers',
    db.Column('follower_id',db.Integer,db.ForeignKey('user.id'),),
    db.Column('followed_id',db.Integer,db.ForeignKey('user.id')))
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    User_name=db.Column(db.String(500),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    notes=db.relationship('Blog',backref='poster')
    followed = db.relationship(
        'User', secondary=Followers,
        primaryjoin=(Followers.c.follower_id == id),
        secondaryjoin=(Followers.c.followed_id == id),
        backref=db.backref('Followers', lazy='dynamic'), lazy='dynamic')
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
        Followers.c.followed_id == user.id).count() > 0
        

    # for relationship we use class
class Blog(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(500),nullable=False)
    Desc=db.Column(db.String(10000),nullable=False)
    date_created=db.Column(db.DateTime(timezone=True),default=func.now())
    blog_pic=db.Column(db.String(50))
    likes=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    comments=db.relationship('Comment',backref="Blog")
    
    # refference of any column always dn by small letter as table name is small 
    def __repr__(self) ->str:
        return f"{self.sno} - {self.title} -{self.Desc}"
    
    
    
class Comment(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String(50))
    Blog_id=db.Column(db.Integer,db.ForeignKey('blog.sno'),nullable=False)


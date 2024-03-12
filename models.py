import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL=" https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png"


"""Models for Blogly."""

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)
    
    imgUrl = db.Column(db.Text,
                       nullable=False,
                       default= DEFAULT_IMAGE_URL
                       )
    @property
    def full_name(self):

        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):
    __tablename__="posts"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement= True)
    title = db.Column(db.Text,
                     nullable=False)
    content = db.Column(db.Text,
                        nullable = False)
    created_at = db.Column(db.datetime,
                        nullable = False,
                        default = datetime.datetime.now)
    users_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable = False)
    

class Tag(db.Model):
        __tablename__= "tags"

        id = db.Column(db.Integer, primary_key= True,
                       autoincrement= True)
        name = db.Column(db.Text,
                         nullable = False,
                         unique = True)
        
        post = db.relationship('Post',
                               secondary="post_tag",
                               backref ="tags")
        
class PostTag(db.Model):
         __tablename__= "post_tag"
         post_id = db.Column(db.Integer,
                        db.ForeignKey('post.id'),
                        nullable = False)
         tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tag.id'),
                       nullable = False)
    
    

def connect_db(app):
    """connects database to flask app"""
    
    db.app = app
    db.init_app(app)
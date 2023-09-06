from datetime import datetime


from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(13), unique=True, nullable=False)
    image_file_url = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)


class PostField(db.Model):
    __tablename__ = "postfield"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    
    

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.relationship("User", lazy=True)
    field = db.relationship("PostField", lazy=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(120), nullable=True)


class PostImage(db.Model):
    __tablename__ = "postimage"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.relationship("Post", lazy=True)
    image_url = db.Column(db.String(60), unique=True, nullable=False)


    


from app import app

with app.app_context() as ctx:
    db.create_all()
from datetime import datetime

from app.extensions import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(13), unique=True, nullable=False)
    image_file_url = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)


class PostField(db.Model):
    __tablename__ = "postfield"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    posts = db.relationship("Post", backref="field", lazy=True)


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey("postfield.id"), nullable=False)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    images = db.relationship("PostImage", backref="post", lazy=True)


class PostImage(db.Model):
    __tablename__ = "postimage"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    image_url = db.Column(db.String(60), unique=True, nullable=False)

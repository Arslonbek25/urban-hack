import os
import secrets
from http import HTTPStatus

from flask import request, url_for
from flask_login import current_user, login_user, logout_user

from app import app, bcrypt, db
from app.models import User
from app.utils import login_required
from app.validation import (
    LoginSchema,
    RegisterSchema,
    RequestResetSchema,
    ResetPasswordSchema,
    UpdateAccountSchema,
)


@app.get("/account")
@login_required
def account():
    return current_user.dict


@app.post("/account")
@login_required
def update_account():
    data = request.get_json()
    if err := UpdateAccountSchema().validate(data):
        return err, HTTPStatus.BAD_REQUEST

    current_user.username = data["username"]
    current_user.email = data["email"]
    db.session.commit()
    return current_user.dict


@app.post("/register")
def register():
    if current_user.is_authenticated:
        return {"message": "You are already logged in"}, HTTPStatus.BAD_REQUEST

    data = request.get_json()
    if err := RegisterSchema().validate(data):
        return err, HTTPStatus.BAD_REQUEST

    hashed_pwd = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(
        username=data["username"].strip(),
        email=data["email"],
        password=hashed_pwd,
    )
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=data["remember"])
    return user.dict


@app.post("/login")
def login():
    if current_user.is_authenticated:
        return {"message": "You are already logged in"}, HTTPStatus.BAD_REQUEST

    data = request.get_json()
    if err := LoginSchema().validate(data):
        return err, HTTPStatus.BAD_REQUEST

    user = User.query.filter_by(email=data["email"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        login_user(user, remember=data["remember"])
        return user.dict
    return {"message": "Wrong email or password"}, HTTPStatus.UNAUTHORIZED


@app.post("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return {"message": "Logout successful"}
    return {"message": "You are already logged out"}

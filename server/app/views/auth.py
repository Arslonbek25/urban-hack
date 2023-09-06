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
        return err

    current_user.username = data["username"]
    current_user.email = data["email"]
    db.session.commit()
    return current_user.dict


@app.post("/register")
def register():
    if current_user.is_authenticated:
        return {"error": "You are already logged in"}, HTTPStatus.BAD_REQUEST

    data = request.get_json()
    if err := RegisterSchema().validate(data):
        return err

    hashed_pwd = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(
        username=data["username"].strip(),
        email=data["email"],
        password=hashed_pwd,
        contact=data["contact"],
    )
    db.session.add(user)
    db.session.commit()
    return "user created"
    # return user.dict


@app.post("/login")
def login():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return {"error": "You are already logged in"}, HTTPStatus.BAD_REQUEST

    data = request.get_json()
    if err := LoginSchema().validate(data):
        return err

    user = User.query.filter_by(email=data["email"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        login_user(user, remember=data["remember"])
        return "U in"
        # return user.dict
    return {"error": "Wrong email or password"}, HTTPStatus.UNAUTHORIZED


@app.post("/logout")
def logout():
    logout_user()
    return {"message": "Logout successful"}

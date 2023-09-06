from flask_login import current_user
from marshmallow import Schema, ValidationError, fields, validate, validates

from app.models import User


def length(min=None, max=None):
    def func(value):
        stripped = value.strip()
        length = len(stripped)
        if min and min > length:
            raise ValidationError(f"Length must be at least {min}.")
        if max and max < length:
            raise ValidationError(f"Length must be at most {max}.")

    return func


class RegisterSchema(Schema):
    username = fields.String(required=True, validate=length(min=2, max=20))
    contact = fields.String(required=True, validate=length(min=2, max=13))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.String(required=True, validate=validate.Length(min=5))

    @validates("username")
    def validate_username(self, value):
        if User.query.filter_by(username=value).first():
            raise ValidationError("This username already exists")

    @validates("email")
    def validate_email(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError("This email already exists")


class LoginSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.String(required=True, validate=validate.Length(min=5))
    remember = fields.Boolean(required=True, truthy={True}, falsy={False})


class UpdateAccountSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=2, max=20))
    email = fields.Email(required=True, validate=validate.Length(max=120))

    @validates("username")
    def validate_username(self, value):
        taken = (
            current_user.username != value
            and User.query.filter_by(username=value).first()
        )
        if taken:
            raise ValidationError("This username already exists")

    @validates("email")
    def validate_email(self, value):
        taken = (
            current_user.email != value and User.query.filter_by(email=value).first()
        )
        if taken:
            raise ValidationError("This email already exists")


class AddTodoSchema(Schema):
    title = fields.String(required=True, validate=length(min=3, max=50))
    description = fields.String(validate=length(max=200))
    due = fields.DateTime()


class RequestResetSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=120))

    @validates("email")
    def validate_email(self, value):
        if not User.query.filter_by(email=value).first():
            raise ValidationError("This email does not exist")


class ResetPasswordSchema(Schema):
    password = fields.String(required=True, validate=validate.Length(min=5))
    confirm_password = fields.String(required=True, validate=validate.Equal("password"))

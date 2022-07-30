import re

from marshmallow import fields
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

from ..model import User
from ..schema import UserSchema
from .base import crud
from ..util import abort, generate_token


def validata_email(email):
    regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    if re.fullmatch(regex, email):
        return True
    return False


def pre_add(user, se):
    if not validata_email(user.email):
        abort("Email is not valid", 400)
    user.password = generate_password_hash(user.password, method="sha256")
    user.uuid = str(uuid.uuid4())
    return user


def pre_put(curr_user, new_user, se):
    if "email" in new_user.keys():
        if not validata_email(new_user["email"]):
            abort("Email is not valid", 400)
    if "password" in new_user.keys():
        new_user["password"] = generate_password_hash(new_user["password"], method="sha256")


get_all, get, post, put, delete = crud(User, UserSchema, [pre_add, pre_put])


def login():
    r = connexion.request.json
    username = r.get("username", None)
    password = r.get("password", None)
    if username is None:
        abort("Need username to login", 401)
    if password is None:
        abort("Need password to login", 401)
    user = User._get(username=username)
    if user is None:
        abort(f"Username or password is wrong", 401)
    if check_password_hash(user.password, password):
        return generate_token(user.uuid)
    else:
        abort(f"Username or password is wrong", 401)

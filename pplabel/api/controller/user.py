import re
import logging

import sqlalchemy
from marshmallow import fields

from ..model import User
from ..schema import UserSchema
from .base import crud
from . import label
from ..util import abort


def validata_email(email):
    regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    if re.fullmatch(regex, email):
        return True
    return False


def pre_add(user, se):
    if not validata_email(user.email):
        abort("Email is not valid", 400)
    return user


def pre_put(curr_user, new_user, se):
    if "email" in new_user.keys():
        if not validata_email(new_user["email"]):
            abort("Email is not valid", 400)


get_all, get, post, put, delete = crud(User, UserSchema, [pre_add])

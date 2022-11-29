import functools
import time

import connexion
import sqlalchemy as sa

from paddlelabel.util import camel2snake

# sa default to nullable=True
nncol = functools.partial(sa.Column, nullable=False)

# TODO: settle on how to use detail and title
def abort(detail: str, status: int, title: str = ""):
    detail = detail.replace("\n", " ")
    title = title.replace("\n", " ")
    raise connexion.exceptions.ProblemException(
        detail=detail,
        title=title if len(title) != 0 else detail,
        status=status,
        headers={"detail": detail},
    )


# TODO: move to config
JWT_ISSUER = "paddlelabel"
JWT_SECRET = "change_this"
JWT_LIFETIME_SECONDS = 43200  # 12h
JWT_ALGORITHM = "HS256"


def generate_token(uuid):
    timestamp = int(time.time())
    payload = {
        "iss": JWT_ISSUER,
        "iat": timestamp,
        "exp": timestamp + JWT_LIFETIME_SECONDS,
        "sub": uuid,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise Unauthorized from e


def parse_order_by(modal, order_by):
    order_by = order_by.split(" ")
    if len(order_by) == 2:
        key, sort_dir = order_by
        # print(key, sort_dir)
        if "asc" in sort_dir:
            sort_dir = "asc"
        else:
            sort_dir = "desc"
    else:
        key = order_by[0]
        sort_dir = "acs"
    key = camel2snake(key)

    try:
        order = getattr(getattr(modal, key), sort_dir)()
    except:
        order = modal.created.asc()
    return order

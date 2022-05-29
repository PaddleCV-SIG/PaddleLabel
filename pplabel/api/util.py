import functools
import random
import time

import connexion
import sqlalchemy as sa

# sa default to nullable=True
nncol = functools.partial(sa.Column, nullable=False)

# TODO: settle on how to use detail and title
def abort(detail, status, title=""):
    raise connexion.exceptions.ProblemException(
        detail=detail, title=title, status=status, headers={"message": detail}
    )


# TODO: move to config
JWT_ISSUER = "pplabel"
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

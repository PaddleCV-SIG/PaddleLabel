import functools

import connexion
import sqlalchemy as sa

# sa default to nullable=True
nncol = functools.partial(sa.Column, nullable=False)


def abort(msg, status):
    raise connexion.exceptions.ProblemException(
        title=msg, status=status, headers={"message": msg}
    )

import functools

import connexion
import sqlalchemy as sa

# sa default to nullable=True
nncol = functools.partial(sa.Column, nullable=False)


# TODO: settle on how to use detail and title
def abort(detail, status, title=""):
    raise connexion.exceptions.ProblemException(
        detail=detail, title=title, status=status, headers={"message": detail}
    )

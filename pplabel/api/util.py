import functools

import sqlalchemy as sa

# sa default to nullable=True
nncol = functools.partial(sa.Column, nullable=False)

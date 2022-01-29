from datetime import datetime

from pplabel.serve import db
from pplabel.api.util import nncol

immutable_properties = ["created", "modified"]

# class BaseModel(db.Model):
#     created = nncol(db.DateTime, default=datetime.utcnow)
#     modified = nncol(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

import json
import marshmallow as mm


class S(mm.Schema):
    username = mm.fields.Str()
    password = mm.fields.Str()
    user_role = mm.fields.Str()
    access_token = mm.fields.Str()
    refresh_token = mm.fields.Str()


d = {"username": "test1", "password": "test1pswd", "user_role": "admin"}
print(type(d))
# S().load(json.dumps(d))
print(type(json.loads(json.dumps(d))))
S().load(json.loads(json.dumps(d)))

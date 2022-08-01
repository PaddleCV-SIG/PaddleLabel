import time

from flask import abort, session, request

import paddlelabel
from paddlelabel.config import app, request_id_timeout

from . import controller
from .model import Project, Label, Task, Data, Annotation, TaskCategory
from .util import decode_token
from . import rpc

# TODO: is this specific to flask or is connexion function
@app.before_request
def check_request_id():
    request_id = request.headers.get("request_id", None)
    if request_id is None or len(request_id) == 0:
        return
    curr_time = time.time()
    if "request_ids" not in session:
        session["request_ids"] = [(curr_time, request_id)]
        return
    session["request_ids"] = list(
        filter(
            lambda item: curr_time - item[0] < request_id_timeout,
            session["request_ids"],
        )
    )
    exist = False
    for ts, id in session["request_ids"]:
        if id == request_id:
            exist = True
    session["request_ids"].append((curr_time, request_id))
    if exist:
        abort(409, f"Duplicate request from {curr_time - ts}s ago")

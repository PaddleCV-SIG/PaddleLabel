import time

from flask import abort, session, request

from pplabel.config import app
from pplabel.config import request_id_timeout


@app.before_request
def check_request_id():
    request_id = request.headers.get("request_id", None)
    if request_id is None:
        return
    curr_time = time.time()
    if "request_ids" not in session:
        session["request_ids"] = [(curr_time, request_id)]
        return
    session["request_ids"] = list(filter(
        lambda item: curr_time - item[0] < request_id_timeout, session["request_ids"]
    ))
    for ts, id in session["request_ids"]:
        if id == request_id:
            abort(409, f"Duplicate request from {curr_time - ts}s ago")

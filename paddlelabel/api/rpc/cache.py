# -*- coding: utf-8 -*-
import connexion
import time

cache_dict = {}


def create_cache():
    content = connexion.request.json["content"]
    global cache_dict
    cache_id = str(time.time())
    cache_dict[cache_id] = content
    # print(cache_id, content)
    return {"cache_id": cache_id}


def get_cache(cache_id):
    # print(cache_id, type(cache_id), cache_dict)
    content = cache_dict.get(cache_id, None)
    if content is None:
        return {"title": f"no cache record with cache_id {cache_id} found"}, 404
    return {"content": content}

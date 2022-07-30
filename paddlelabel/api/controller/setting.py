import json

from ..model import TaskCategory

from paddlelabel.config import se


# TODO: change task_categories to project_category
def init_site_settings(json_path):
    settings = json.loads(open(json_path, "r").read())
    task_categories = settings["site"]["task_categories"]
    for idx, (cat, handler) in task_categories.items():
        idx = int(idx)
        curr_cat = TaskCategory.query.filter(TaskCategory.task_category_id == idx).one_or_none()
        if curr_cat is None:
            curr_cat = TaskCategory(idx, cat, handler)
            se.add(curr_cat)
            se.commit()

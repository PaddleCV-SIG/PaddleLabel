import json

from .model import TaskCategory

from pplabel.config import se


def init_site_settings(json_path):
    settings = json.loads(open(json_path, "r").read())
    task_categories = settings["site"]["task_categories"]
    for idx, (cat, handler) in task_categories.items():
        idx = int(idx)
        curr_cat = TaskCategory.query.filter(
            TaskCategory.task_category_id == idx
        ).one_or_none()
        print(TaskCategory.query.all())
        print("_+_+_+_+_+_+", cat)
        if curr_cat is None:
            curr_cat = TaskCategory(idx, cat, handler)
            se.add(curr_cat)
            print("add task", TaskCategory(idx, cat, handler))
            se.commit()
    print("+++++++++++ All TackCategories: ", TaskCategory.query.all())

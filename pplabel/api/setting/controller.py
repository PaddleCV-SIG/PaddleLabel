import json

from .model import TaskCategory

from pplabel.config import se


def init_site_settings(json_path):
    settings = json.loads(open(json_path, "r").read())
    task_categories = settings["site"]["task_categories"]
    for idx, (cat, handler) in task_categories.items():
        print("-----------", TaskCategory(int(idx), cat, handler))
        se.add(TaskCategory(int(idx), cat, handler))
        se.commit()
        print("+++++++++++ All TackCategories: ", TaskCategory.query.all())

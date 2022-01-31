import os
import os.path as osp
import json

from pplabel.config import db
from pplabel.api import Project, Task, Data, Annotation, Label
from pplabel.api.schema import ProjectSchema
from ..util import create_dir, listdir


class Classification:
    def __init__(self, project):
        curr_project = Project._get(project_id=project.project_id)
        if curr_project is None:
            db.session.add(project)
            db.session.commit()
        self.project = project

    def single_class_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."]},
    ):
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir

        success, res = create_dir(data_dir)
        if not success:
            return False, res
        data_paths = listdir(data_dir, filters)
        print(data_paths)

        def get_tasks(datas):
            for data in datas:
                # BUG: root dir
                label = osp.basename(osp.dirname(data))
                yield data, [label]

        for data_path, label in get_tasks(data_paths):
            print(data_path, label)
            self.add_task([data_path], label)

    def add_tasks(self, data_paths: list, annotation_names: list):
        for d, a in zip(data_paths, annotation_names):
            self.add_task(d, a)

    def add_task(self, data_paths: list, annotation_names: list):
        datas = []
        for data_path in data_paths:
            data_path = data_path[len(self.project.data_dir) :]
            datas.append(Data(path=data_path, slice_count=1))
        annotations = []
        for ann in annotation_names:
            label = Label.query.filter(Label.name == ann).one_or_none()
            # TODO: label is None
            annotations.append(
                Annotation(
                    label_id=label.label_id,
                    project_id=self.project.project_id,
                    slice_id=0,
                )
            )
        task = Task(
            project_id=self.project.project_id,
            datas=datas,
            annotations=annotations,
        )

        db.session.add(task)
        db.session.commit()


def main():
    pj_info = {
        "name": "Single Class Classification Example",
        "data_dir": "/home/lin/Desktop/data/pplabel/single_clas_toy/PetImages/",
        "description": "Example Project Descreption",
        "label_dir": "",
        "other_settings": "{'some_property':true}",
        "task_category_id": 1,
        "labels": [{"id": 1, "name": "Cat"}, {"id": 2, "name": "Dog"}],
    }
    project = ProjectSchema().load(pj_info)

    clas_project = Classification(project)

    clas_project.single_class_importer(
        filters={"exclude_prefix": ["."], "exclude_postfix": [".db"]}
    )

    tasks = Task.query.all()
    for task in tasks:
        print("tasktasktasktasktasktasktasktask", task)


if __name__ == "__main__":
    main()

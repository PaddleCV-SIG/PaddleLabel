import os
import os.path as osp
import json

from pplabel.config import db
from pplabel.api import Project, Task, Data, Annotation, Label
from pplabel.api.schema import ProjectSchema
from .util import create_dir, listdir, ComponentManager


class Classification:
    importers = ComponentManager()
    exporters = ComponentManager()

    def __init__(self, project):
        curr_project = Project._get(project_id=project.project_id)
        if curr_project is None:
            db.session.add(project)
            db.session.commit()
        self.project = project

    @importers.add_component
    def single_class_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."]},
    ):
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir

        # TODO: if data_dir is not poroject.data_dir, move data to project.data_dir
        success, res = create_dir(data_dir)
        if not success:
            return False, res
        data_paths = listdir(data_dir, filters)

        def get_tasks(datas):
            for data in datas:
                # BUG: root dir
                label = osp.basename(osp.dirname(data))
                yield data, [label]

        for data_path, label in get_tasks(data_paths):
            self.add_task([data_path], label)

    @importers.add_component
    def multi_class_importer(
        self,
        data_dir=None,
        label_path=None,
        filters={"exclude_prefix": ["."]},
    ):
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir
        if label_path is None:
            label_path = project.label_dir
        success, res = create_dir(data_dir)
        if not success:
            return False, res
        data_paths = listdir(data_dir, filters)
        label_lines = open(label_path, "r").readlines()
        label_lines = [l.strip() for l in label_lines if len(l.strip()) != 0]
        labels_dict = {}
        for label in label_lines:
            cols = label.split(" ")
            labels_dict[cols[0]] = cols[1:]
        for data_path in data_paths:
            id = data_path[len(project.data_dir) :]
            labels = labels_dict[id]
            self.add_task([data_path], labels)

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

    def single_clas_exporter(self, export_dir):
        pass


def single_clas():
    pj_info = {
        "name": "Single Class Classification Example",
        "data_dir": "/home/lin/Desktop/data/pplabel/demo/single_clas/PetImages/",
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


def multi_clas():
    pj_info = {
        "name": "Multi Class Classification Example",
        "data_dir": "/home/lin/Desktop/data/pplabel/demo/multi_clas/PetImages/",
        "description": "Example Project Descreption",
        "label_dir": "/home/lin/Desktop/data/pplabel/demo/multi_clas/label.txt",
        "other_settings": "{'some_property':true}",
        "task_category_id": 1,
        "labels": [
            {"id": 1, "name": "Cat"},
            {"id": 2, "name": "Dog"},
            {"id": 3, "name": "Small"},
            {"id": 4, "name": "Large"},
        ],
    }
    project = ProjectSchema().load(pj_info)

    clas_project = Classification(project)

    clas_project.multi_class_importer(
        filters={"exclude_prefix": ["."], "exclude_postfix": [".db"]}
    )

    tasks = Task.query.all()
    for task in tasks:
        print("tasktasktasktasktasktasktasktask", task)
    print("------------------", dir(Classification.importers["single_class_importer"]))

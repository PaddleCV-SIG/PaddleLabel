import os
import os.path as osp

from pplabel.config import db, task_test_basedir
from pplabel.api import Project, Task, Data, Annotation, Label
from pplabel.api.schema import ProjectSchema
from .util import create_dir, listdir, copy, copytree, ComponentManager
from .base import BaseTask


class Classification(BaseTask):
    importers = ComponentManager()
    exporters = ComponentManager()

    @importers.add_component
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
        for data_path in listdir(data_dir, filters):
            print(data_path)
            label_name = osp.basename(osp.dirname(data_path))
            self.add_task([data_path], [{"label_name": label_name}])
        if data_dir != project.data_dir:
            copytree(data_dir, project.data_dir)

    @importers.add_component
    def multi_class_importer(
        self,
        data_dir=None,
        label_path=None,
        delimiter=" ",
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
        if label_path is not None and not osp.exists(label_path):
            return False, f"label_path {label_path} doesn't exist"
        data_paths = listdir(data_dir, filters)
        label_lines = open(label_path, "r").readlines()
        label_lines = [l.strip() for l in label_lines if len(l.strip()) != 0]
        labels_dict = {}
        for label in label_lines:
            cols = label.split(delimiter)
            labels_dict[cols[0]] = cols[1:]
        for data_path in data_paths:
            data_path = data_path[len(project.data_dir) :]
            labels = labels_dict[data_path]
            self.add_task([data_path], [{"label_name": name} for name in labels])

    @exporters.add_component
    def single_clas_exporter(self, export_dir):
        project = self.project
        labels = Label._get(project_id=project.project_id, many=True)
        for label in labels:
            dir = osp.join(export_dir, label.name)
            create_dir(dir)

        tasks = Task._get(project_id=project.project_id, many=True)
        for task in tasks:
            for ann in task.annotations:
                dst = osp.join(export_dir, ann.label.name)
                for data in task.datas:
                    copy(osp.join(project.data_dir, data.path), dst)

    @exporters.add_component
    def multi_clas_exporter(self, export_dir):
        project = self.project
        create_dir(export_dir)
        tasks = Task._get(project_id=project.project_id, many=True)
        f = open(osp.join(export_dir, "label.txt"), "w")
        for task in tasks:
            for data in task.datas:
                copy(osp.join(project.data_dir, data.path), export_dir)
                line = data.path
                for ann in task.annotations:
                    line += " " + ann.label.name
                print(line, file=f)


def single_clas():
    pj_info = {
        "name": "Single Class Classification Example",
        "data_dir": osp.join(task_test_basedir, "clas_single/PetImages/"),
        "description": "Example Project Descreption",
        "other_settings": "{'some_property':true}",
        "task_category_id": 1,
        "labels": [{"id": 1, "name": "Cat"}, {"id": 2, "name": "Dog"}],
    }
    project = ProjectSchema().load(pj_info)

    clas_project = Classification(project)

    clas_project.single_class_importer(
        filters={"exclude_prefix": ["."], "exclude_postfix": [".db"]}
    )
    print("------------------ all tasks ------------------ ")
    for task in Task._get(project_id=project.project_id, many=True):
        print(task)

    clas_project.single_clas_exporter(
        osp.join(task_test_basedir, "export/clas_single_export")
    )


def multi_clas():
    pj_info = {
        "name": "Multi Class Classification Example",
        "data_dir": osp.join(task_test_basedir, "clas_multi/PetImages/"),
        "description": "Example Project Descreption",
        "label_dir": osp.join(task_test_basedir, "clas_multi/label.txt"),
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

    clas_project.single_clas_exporter(
        osp.join(task_test_basedir, "export/clas_multi_folder_export")
    )

    clas_project.multi_clas_exporter(
        osp.join(task_test_basedir, "export/clas_multi_file_export")
    )
    tasks = Task.query.all()
    for task in tasks:
        print("tasktasktasktasktasktasktasktask", task)

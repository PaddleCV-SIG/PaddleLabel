import os
import os.path as osp

from pplabel.config import db, task_test_basedir
from pplabel.api import Project, Task, Data, Annotation, Label
from pplabel.api.schema import ProjectSchema
from .util import create_dir, listdir, copy, copytree, ComponentManager, image_extensions
from .base import BaseTask


class Segmentation(BaseTask):
    def __init__(self, project):
        super().__init__(project)
        self.importers = {
            "gray_scale": self.gray_scale_importer,
        }
        self.exporters = {
            "gray_scale": self.single_class_exporter,
        }

    def gray_scale_importer(
        self,
        data_dir=None,
        label_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir
        if label_path is None:
            label_path = project.label_dir

        # 1. if data_dir/labels.txt exists, import labels
        # TODO: last string as color
        if label_path is not None and osp.exists(label_path):
            labels = open(label_path, "r").readlines()
            labels = [l.strip() for l in labels if len(l.strip()) != 0]
            for lab in labels:
                self.add_label(lab)

        # 2. import records
        create_dir(data_dir)
        for data_path in listdir(data_dir, filters):
            if data_path == label_path:
                continue
            if project.data_dir in data_path:
                data_path = osp.relpath(data_path, project.data_dir)
            label_name = osp.basename(osp.dirname(data_path))
            self.add_task([data_path], [[{"label_name": label_name}]])
            print(f"==== {data_path} imported ====")

        # 3. move data
        if data_dir != project.data_dir:
            copytree(data_dir, project.data_dir)

    def gray_scale_exporter(self, export_dir):
        create_dir(export_dir)

        project = self.project
        labels = Label._get(project_id=project.project_id, many=True)
        labels.sort(key=lambda l: l.id)
        label_idx = {}
        for idx, label in enumerate(labels):
            label_idx[label.name] = idx
        with open(osp.join(export_dir, "labels.txt"), "w") as f:
            for lab in labels:
                print(lab.name, file=f)

        for label in labels:
            dir = osp.join(export_dir, label.name)
            create_dir(dir)

        set_names = ["train", "validation", "test"]
        set_files = [open(osp.join(export_dir, f"{n}.txt"), "w") for n in set_names]
        tasks = Task._get(project_id=project.project_id, many=True)
        for task in tasks:
            for data in task.datas:
                label_name = ""
                if len(data.annotations) == 1:
                    label_name = data.annotations[0].label.name
                    print(
                        f"{osp.join(label_name, osp.basename(data.path))} {label_idx[label_name]}",
                        file=set_files[task.set],
                    )
                dst = osp.join(export_dir, label_name)
                copy(osp.join(project.data_dir, data.path), dst)

        for f in set_files:
            f.close()


def test():
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
    print(clas_project.importers[0])


# def single_clas():
#     pj_info = {
#         "name": "Single Class Classification Example",
#         "data_dir": osp.join(task_test_basedir, "clas_single/PetImages/"),
#         "description": "Example Project Descreption",
#         "other_settings": "{'some_property':true}",
#         "task_category_id": 1,
#         "labels": [{"id": 1, "name": "Cat"}, {"id": 2, "name": "Dog"}],
#     }
#     project = ProjectSchema().load(pj_info)
#
#     clas_project = Classification(project)
#
#     clas_project.importers[0](filters={"exclude_prefix": ["."], "exclude_postfix": [".db"]})
#     print("------------------ all tasks ------------------ ")
#     for task in Task._get(project_id=project.project_id, many=True):
#         print(task)
#
#     clas_project.single_clas_exporter(osp.join(task_test_basedir, "export/clas_single_export"))
#
#
# def multi_clas():
#     pj_info = {
#         "name": "Multi Class Classification Example",
#         "data_dir": osp.join(task_test_basedir, "clas_multi/PetImages/"),
#         "description": "Example Project Descreption",
#         "label_dir": osp.join(task_test_basedir, "clas_multi/label.txt"),
#         "other_settings": "{'some_property':true}",
#         "task_category_id": 1,
#         "labels": [
#             {"id": 1, "name": "Cat"},
#             {"id": 2, "name": "Dog"},
#             {"id": 3, "name": "Small"},
#             {"id": 4, "name": "Large"},
#         ],
#     }
#     project = ProjectSchema().load(pj_info)
#
#     clas_project = Classification(project)
#
#     clas_project.multi_class_importer(filters={"exclude_prefix": ["."], "exclude_postfix": [".db"]})
#
#     clas_project.single_clas_exporter(
#         osp.join(task_test_basedir, "export/clas_multi_folder_export")
#     )
#
#     clas_project.multi_clas_exporter(osp.join(task_test_basedir, "export/clas_multi_file_export"))
#     tasks = Task.query.all()
#     for task in tasks:
#         print("=======task=======", task)

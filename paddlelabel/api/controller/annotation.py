import connexion

from .base import crud
from ..model import Annotation, Task, Project, Data
from ..schema import AnnotationSchema
from ..util import abort

from paddlelabel.config import db

# TODO: don't create label if exists.


def pre_add(annotation, se):
    _, data = Data._exists(annotation.data_id)
    _, task = Task._exists(data.task_id)
    annotation.task_id = data.task_id
    annotation.project_id = task.project_id

    return annotation


get_all, get, post, put, delete = crud(Annotation, AnnotationSchema, [pre_add])


def get_by_project(project_id):
    Project._exists(project_id)
    anns = Annotation._get(project_id=project_id, many=True)
    return AnnotationSchema(many=True).dump(anns), 200


def get_by_task(task_id):
    Task._exists(task_id)
    anns = Annotation._get(task_id=task_id, many=True)
    return AnnotationSchema(many=True).dump(anns), 200


def get_by_data(data_id):
    Data._exists(data_id)
    anns = Annotation._get(data_id=data_id, many=True)
    return AnnotationSchema(many=True).dump(anns), 200


def set_all_by_data(data_id):
    """Receive all annotataions under a data record from front end and update database

    Args:
        data_id (int): data_id
    """

    # 1. ensure data exists
    _, data = Data._exists(data_id)

    # 2. load and parse all new anns
    schema = AnnotationSchema()
    anns = connexion.request.json
    for idx in range(len(anns)):
        del anns[idx]["label"]
        anns[idx] = schema.load(anns[idx])
    curr_anns = Annotation._get(data_id=data.data_id, many=True)  # query before the first edit
    curr_ann_ids = set([ann.annotation_id for ann in curr_anns])

    # 3. add new ann and update existing ann
    task = Task._get(task_id=data.task_id)
    keep_ann_ids = []  # anns to keep, newly created anns don't need to be included in this
    for ann in anns:
        # if ann doesn't have id or id not in curr ids, it's new
        if ann.annotation_id is None or ann.annotation_id not in curr_ann_ids:
            ann.annotation_id = None
            ann.task_id = task.task_id
            ann.project_id = task.project_id
            db.session.add(ann)
        else:
            keep_ann_ids.append(ann.annotation_id)
            ann_dict = schema.dump(ann)
            del ann_dict["created"]
            del ann_dict["modified"]
            del ann_dict["annotation_id"]
            del ann_dict["label"]
            Annotation.query.filter(Annotation.annotation_id == ann.annotation_id).update(ann_dict)

    # 4. remove anns that are in db, but not in anns
    # print("curr_anns", curr_anns)
    for curr_ann in curr_anns:
        if curr_ann.annotation_id not in keep_ann_ids:
            db.session.delete(curr_ann)

    db.session.commit()

    curr_anns = Annotation._get(data_id=data.data_id, many=True)
    schema = AnnotationSchema(many=True)
    return schema.dump(curr_anns), 200


def delete_by_data(data_id):
    anns = Annotation._get(data_id=data_id, many=True)
    for ann in anns:
        db.session.delete(ann)
    db.session.commit()


def set_all_by_task_and_frontend(task_id):
    _, task = Task._exists(task_id)
    # 删除task关联的所有annotation
    current_anns = Annotation._get(task_id=task_id, many=True)
    for cann in current_anns:
        db.session.delete(cann)
    # 插入新annotation
    anns = connexion.request.json
    schema = AnnotationSchema()
    for ann in anns:
        ann = schema.load(ann)
        ann.task_id = task.task_id
        ann.project_id = task.project_id
        task.annotations.append(ann)
    db.session.commit()

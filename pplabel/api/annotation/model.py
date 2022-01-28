# from datetime import datetime
#
# from sqlalchemy import event
#
# from pplabel.config import db
# from pplabel.api.util import nncol
#
#
# class Task(db.Model):
#     __tablename__ = "task"
#     __table_args__ = {"comment": "Contains all the tasks"}
#     task_id = nncol(db.Integer(), primary_key=True)
#     project_id = nncol(
#         db.Integer(), db.ForeignKey("project.project_id", ondelete="CASCADE")
#     )
#     # data_paths = nncol(db.String(), unique=True)
#     datas = db.relationship("Data", backref="task")
#     project = db.relationship("Project")
#     # slice_count = nncol(db.Integer())
#     # annotation
#     created = nncol(db.DateTime, default=datetime.utcnow)
#     modified = nncol(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#
#
# # @event.listens_for(Task, 'after_insert')
# # def receive_after_insert(mapper, connection, target):
# #     print()
# @event.listens_for(Task.task_id, "set")
# def receive_set(target, value, oldvalue, initiator):
#     print("44444444444444", target, value, oldvalue, initiator)

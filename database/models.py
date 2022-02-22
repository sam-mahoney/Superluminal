from database.db import db


# Define the Task object


# ------------------------------
# |    task_id    |    UUID    |
# |   task_type   |   string   |
# |     args      |    list    |
#
class Task(db.DynamicDocument):
    task_id = db.StringField(required=True)


class Result(db.DynamicDocument):
    result_id = db.StringField(required=True)
    task_id = db.StringField(required=True)

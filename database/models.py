from database.db import db


# Define the Task object

# [!] Notes
# Why would it be a benefit to use a dynamic document here?
# Tasks should be clearly defined objects
# ------------------------------
# |    task_id    |    UUID    |
# |   task_type   |   string   |
# |     args      |    list    |
#
class Task(db.DynamicDocument):
    task_id = db.StringField(required=True)

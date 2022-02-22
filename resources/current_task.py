from flask import Response
from flask_restful import Resource

from database.models import Task


class CurrentTask(Resource):
    """
    Represents a queue
    """
    def get(self):
        # Responds with the oldest task in the database
        next_task_in_queue = Task.objects().order_by('date')[0]
        if not next_task_in_queue['executing']:
            next_task_in_queue['executing'] = True
            next_task_in_queue.save()
        # Return when already executing
        # Implant GETs the task and it sets it to executing
        # Task gets deleted when result is returned
        # Else just send the same task?
        # Implant can check the id and see it it has already received it so it doesn't execute twice
        # Results POST request contains the task_id which enables the server to delete the task
        return Response(next_task_in_queue.to_json(), mimetype="application/json", status=200)

import json

from flask import Response
from flask_restful import Resource

from database.models import Task

from common.types.task_types import Status


class NextTask(Resource):
    """
    Gets the head of the queue
    """
    def get(self):
        # Returns the next Task to execute
        try:
            next_task_in_queue = Task.objects().order_by('date')[0]
        except IndexError:
            print("[!] Queue is empty")
            error = {"status code": "400", "error": "empty queue"}
            return Response(json.dumps(error), status=400)
        if next_task_in_queue['task_status'] == Status.EXECUTING.name:
            print("[!] Requesting new task before returning results of previous task")
            error = {"status code": "400", "error": "RESULTS MUST BE RETURNED BEFORE REQUESTING NEXT TASK"}
            return Response(json.dumps(error), status=400)
        # Check the task is waiting to be executed
        if next_task_in_queue['task_status'] != Status.WAITING.name:
            # If the next Task isn't waiting delete it
            next_task_in_queue.delete()
            print("[!] Queue out of sync - Deleting Task")
            error = {"status code": "503", "error": "Queue out of sync. Retry..."}
            return Response(json.dumps(error), status=503)
        # Set status to executing
        next_task_in_queue['task_status'] = Status.EXECUTING.name
        # Update the Task
        next_task_in_queue.save()
        return Response(next_task_in_queue.to_json(), mimetype="application/json", status=200)

import uuid
import json

from flask import request, Response
from flask_restful import Resource


# TODO - add a description resource
class Tasks(Resource):
    # Returns tasks
    def get(self):
        # TODO - implement get logic
        tasks = {'task_id': '0',
                 'task_type': 'ping'}
        # mimetype: a two-part identifier for file formats and format contents transmitted on the Internet.
        return Response(tasks, mimetype="application/json", status=200)

    # Adds a task
    def post(self):
        # TODO - implement post logic
        # 1. Extract the JSON body from the request
        # 2. Find the number of tasks in the request
        # 3. Add each task to the database
        #   3a. Give each task a uuid
        #   3b.
        # 4. Return task object
        return "POST success", 200

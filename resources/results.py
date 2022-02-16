from flask import request, Response
from flask_restful import Resource


class Results(Resource):
    """
    Description

    Methods
    -------
    get  : returns all results objects to user (CLI)
    post : adds result(s) to the database (implant)
    """
    # List results
    def get(self):
        # TODO - implement get logic
        # Get all the result objects and return them to the user
        # Server -> HTTP -> CLI
        results = {'task_id': 0}
        return Response(results, mimetype="application/json", status=200)

    def post(self):
        # TODO - implement post logic
        # Add result to db
        # Implant -> HTTP -> Server
        result = 0

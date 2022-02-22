import json

from flask import Response
from flask_restful import Resource

from database.models import TaskHistory


class History(Resource):
    """DOCSTRING"""
    def get(self):
        history = TaskHistory.objects().to_json()
        return Response(history, mimetype="application/json", status=200)

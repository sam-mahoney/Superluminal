import json


def parse_request(body):
    return json.loads(json.dumps(body)), len(body)

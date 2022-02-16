from flask_restful import Resource


# API Route for initial testing
class Bing(Resource):
    def get(self):
        return {'bing': '0',
                'bong': '1'}

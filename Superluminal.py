from flask import Flask
from flask_restful import Api

from resources.foo import Foo
from resources.bing import Bing
from resources.tasks import Tasks
from resources.results import Results

# Initialise Flask app and API
app = Flask(__name__)
api = Api(app)

# API routes for testing/debug
api.add_resource(Foo, '/Foo')
api.add_resource(Bing, '/Bing')

# Define the routes for API Resources
api.add_resource(Tasks, '/tasks', endpoint='tasks')
api.add_resource(Results, '/results')


if __name__ == '__main__':
    app.run(debug=True)

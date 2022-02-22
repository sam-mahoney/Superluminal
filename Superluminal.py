from flask import Flask
from flask_restful import Api

from database.db import initialise_db

from resources.foo import Foo
from resources.bing import Bing
from resources.tasks import Tasks
from resources.next_task import NextTask
from resources.results import Results
from resources.history import History

# Initialise Flask app and API
app = Flask(__name__)
api = Api(app)


# Configure database on localhost
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/superluminal'
}

# Initialise database
initialise_db(app)

# API routes for testing/debug
api.add_resource(Foo, '/Foo')
api.add_resource(Bing, '/Bing')

# Define the routes for API Resources
api.add_resource(Tasks, '/tasks', endpoint='tasks')
api.add_resource(NextTask, '/next_task')
api.add_resource(Results, '/results')
api.add_resource(History, '/history')


if __name__ == '__main__':
    app.run(debug=True)

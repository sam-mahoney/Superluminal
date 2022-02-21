from flask_mongoengine import MongoEngine

# Initialise MongoDB
db = MongoEngine()


def initialise_db(app):
    db.init_app(app)

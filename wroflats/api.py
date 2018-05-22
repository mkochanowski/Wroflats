from flask import Flask, json
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_pyfile("config.py")

from resources import *

migrate = Migrate(app, db)
api = Api(app)

from tasks import *

class Index(Resource):
    project_repository = "https://github.com/mkochanowski/wroflats/"
    project_documentation = "https://docs.kochanow.ski/wroflats/"

    def get(self):
        return {
            "repository": self.project_repository,
            "documentation": self.project_documentation
        }

api.add_resource(SubmissionsSingle, '/submissions/<int:identifier>')
api.add_resource(SubmissionsIndex, '/submissions')
# api.add_resource(AreasCheck, '/areas/<string:category>/<string:coordinates>')
# api.add_resource(AreasFiltered, '/areas/<string:category>')
api.add_resource(AreasSingle, '/areas/<int:identifier>')
api.add_resource(AreasIndex, '/areas')
api.add_resource(AuthSignIn, '/auth/signin')
api.add_resource(AuthSignUp, '/auth/signup')
api.add_resource(UsersSingle, '/users/<int:identifier>')
api.add_resource(UsersIndex, '/users')
api.add_resource(GroupsSingle, '/groups/<int:identifier>')
api.add_resource(GroupsIndex, '/groups')
api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(debug=True)
import logging
from flask import request
from flask_restful import Resource, reqparse
from models import *
parser = reqparse.RequestParser()

class Helper:
    @staticmethod
    def normalize_coordinates(coordinates: tuple) -> tuple:
        return coordinates

    def get_or_create_coordinates(self, coordinates: tuple) -> int:
        coordinates = self.normalize_coordinates(coordinates)
        lat, lng = coordinates
        search = Coordinates.query.filter_by(latitude=lat, longitude=lng).first()

        if search:
            return search.id
        
        new_coordinates = Coordinates(
            latitude=lat,
            longitude=lng
        )

        db.session.add(new_coordinates)
        db.session.commit()

        return new_coordinates.id

class SubmissionsIndex(Resource):
    """Operates on all available submissions."""
    schema = SubmissionSchema()

    def get(self):
        """Retrieved a list of all submissions."""
        submissions = Submission.query.all()
        if submissions:
            return self.schema.dump(submissions, many=True).data
        return { "info": "no submissions" }

    def post(self):
        """Adds a new submission."""

        args = parser.parse_args()
        logging.info(args)

        coordinates = (request.json["latitude"], request.json["longitude"])

        helper = Helper()
        coordinates_id = helper.get_or_create_coordinates(coordinates)

        new_submission = Submission(
            category=request.json["category"],
            origin=request.json["origin"],
            title=request.json["title"],
            url=request.json["url"],
            description=request.json["description"],
            price=request.json["price"],
            source_latitude=request.json["latitude"],
            source_longitude=request.json["longitude"],
            coordinates_id=coordinates_id
        )

        db.session.add(new_submission)
        db.session.commit()

        return self.schema.dump(new_submission).data


class SubmissionsSingle(Resource):
    """Operates on a single submission."""
    schema = SubmissionSchema()

    def get(self, identifier: int):
        """Returns details about the requested submission."""
        submission = Submission.query.filter_by(id=identifier).first()
        if submission:
            return self.schema.dump(submission).data
        return { "info": "submission does not exist" }

class AreasIndex(Resource):
    """Operates on an index of all defined areas."""
    schema = AreaSchema()

    def get(self):
        """Returns a list of all areas."""
        areas = Area.query.all()
        if areas:
            return self.schema.dump(areas, many=True).data
        return { "info": "no areas" }

    def post(self):
        """Add a new area."""
        new_area = Area(
            group_id=request.json["group_id"],
            type=request.json["type"],
            center=request.json["center"],
            radius=request.json["radius"]
        )

        db.session.add(new_area)
        db.session.commit()

        return self.schema.dump(new_area).data


class AreasSingle(Resource):
    schema = AreaSchema()

    def get(self, identifier: int):
        area = Area.query.filter_by(id=identifier).first()
        if area:
            return self.schema.dump(area).data
        return { "info": "area does not exist" }

    def patch(self):
        """Update an existing area."""
        pass


class AreasCheck(Resource):
    """Operates on all areas."""

    def post(self, category: str, coordinated: str):
        """Returns whether given coordinates belong to a category type."""

        return True


class AuthSignIn(Resource):
    """Performs the log in procedure."""

    def post(self, token: str):
        pass


class AuthSignUp(Resource):
    """Adds a new user account."""

    def post(self):
        """Creates a new account."""
        schema = UserSchema()

        new_user = User(
            username=request.json["username"],
            full_name=request.json["full_name"],
            password=request.json["password"]
        )

        db.session.add(new_user)
        db.session.commit()

        return schema.dump(new_user).data


class UsersIndex(Resource):
    """Operates on all available users."""
    def get(self):
        """Retrieves a list of all registered users."""
        schema = UserSchema()
        users = User.query.all()
        
        if users:
            return schema.dump(users, many=True).data
        return { "info": "no users" }

class UsersSingle(Resource):
    """Operates on a single user."""
    def get(self, identifier):
        schema = UserSchema()
        user = User.query.filter_by(id=identifier).first()
        
        if user:
            return schema.dump(user).data
        return { "info": "user does not exist" }

class GroupsIndex(Resource):
    schema = GroupSchema()
    
    def get(self):
        groups = Group.query.all()

        if groups:
            return self.schema.dump(groups, many=True).data
        return { "info": "no groups" }

    def post(self):
        new_group = Group(
            title=request.json["title"],
            owner_id=request.json["owner_id"]
        )    

        db.session.add(new_group)
        db.session.commit()

        return self.schema.dump(new_group).data

class GroupsSingle(Resource):
    def get(self, identifier: int):
        schema = GroupSchema()
        group = Group.query.filter_by(id=identifier).first()

        if group:
            return schema.dump(group).data
        return { "info": "group does not exist" }
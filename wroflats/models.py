from api import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)


users_groups_assoc = db.Table(
    'users_groups_assoc',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey(
        'groups.id'), primary_key=True)
)

submissions_pairs_coordinates_assoc = db.Table(
    'submissions_calculated_pairs_assoc',
    db.Column('pair_id', db.Integer, db.ForeignKey(
        'coordinates_pairs.id'), primary_key=True),
    db.Column('submission_id', db.Integer, db.ForeignKey(
        'submissions_calculated.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    full_name = db.Column(db.String(128), unique=False, nullable=True)
    password = db.Column(db.String(200), nullable=False)
    groups = db.relationship('Group', secondary=users_groups_assoc,
                             backref=db.backref('users', lazy=True))
    sessions = db.relationship('Session', backref='user')
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = generate_password_hash(password, method='sha256')

    def __repr__(self) -> str:
        return ''.join([
            f'<User (id={self.id}, username={self.username}, ',
            f'password={self.password}, groups={self.groups}, ',
            f'sessions={self.sessions}, created={self.created})>'
        ])


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(40), default='activated')
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<Group (id={self.id}, title={self.title}, ',
            f'owner_id={self.owner_id}, status={self.status}, ',
            f'created={self.created})>'
        ])


class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    expires = db.Column(db.DateTime, nullable=True,
                        default=None)

    def __repr__(self):
        return ''.join([
            f'<Session (id={self.id}, user_id={self.user_id}, ',
            f'created={self.created}, expires={self.expires})>'
        ])


class Submission(db.Model):
    __tablename__ = 'submissions'
    __bind_key__ = 'scraping'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(40), nullable=True)
    origin = db.Column(db.String(40))
    title = db.Column(db.String(255))
    url = db.Column(db.String(512))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    coordinates_id = db.Column(db.Integer, db.ForeignKey('coordinates.id'))
    is_scraped = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<Submission (id={self.id}, category={self.category}, ',
            f'origin={self.origin}, title={self.title}, url={self.url}, ',
            f'description={self.description}, price={self.price}, ',
            f'coordinates_id={self.coordinates_id}, is_scraped=',
            f'{self.is_scraped}, created={self.created})>'
        ])


class CalculatedSubmission(db.Model):
    __tablename__ = 'submissions_calculated'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    cords_pairs = db.relationship('PairOfCoordinates', secondary=submissions_pairs_coordinates_assoc, backref=db.backref('submissions', lazy=True))
    rating = db.Column(db.Integer)
    parameters = db.Column(db.PickleType)
    status = db.Column(db.String(40))
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<CalculatedSubmission (id={self.id}, submission_id=',
            f'{self.submission_id}, group_id={self.group_id}, ',
            f'rating={self.rating}, parameters={self.parameters}, ',
            f'status={self.status}, created={self.created})>'
        ])


class Action(db.Model):
    __tablename__ = 'actions'

    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey(
        'submissions_calculated.id'))
    action = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<Action (id={self.id}, target_id={self.target_id}, ',
            f'action={self.action}, user_id={self.user_id}, ',
            f'created={self.created})>'
        ])


class Coordinates(db.Model):
    __tablename__ = 'coordinates'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    given_latitude = db.Column(db.Integer)
    given_longitude = db.Column(db.Integer)
    submissions = db.relationship('Submission')
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<Coordinates (id={self.id}, latitude={self.latitude}, ',
            f'longitude={self.longitude}, given_latitude={self.given_latitude}, ',
            f'given_longitude={self.given_longitude}, submissions=',
            f'{self.submissions}, created={self.created})>'
        ])


class PairOfCoordinates(db.Model):
    __tablename__ = 'coordinates_pairs'

    id = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.Integer, db.ForeignKey('coordinates.id'))
    target_id = db.Column(db.Integer, db.ForeignKey('coordinates.id'))
    distance = db.Column(db.Integer)
    time_transit = db.Column(db.Integer)
    time_on_foot = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    calculated = db.Column(db.DateTime, nullable=True,
                           default=None)

    def __repr__(self):
        return ''.join([
            f'<PairOfCoordinates (id={self.id}, origin_id={self.origin_id}, ',
            f'target_id={self.target}, calculated={self.calculated}, ',
            f'submissions={self.submissions}, distance={self.distance}, ',
            f'time_transit={self.time_transit}, time_on_foot=',
            f'{self.time_on_foot}, created={self.created})>'
        ])


class Area(db.Model):
    __tablename__ = 'areas'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    type = db.Column(db.String(40), default='forbidden')
    center = db.Column(db.Integer, db.ForeignKey('coordinates.id'))
    radius = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<Area (id={self.id}, group_id={self.group_id}, type={self.type}, ',
            f'center={self.center}, radius={self.radius}, created={self.created})>'
        ])

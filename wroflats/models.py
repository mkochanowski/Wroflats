from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    groups = db.relationship('Group')
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<User (id={self.id}, username={self.username}, ',
            f'password={self.password}, groups={self.groups}, ',
            f'created={self.created})>'
        ])


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    owner = db.relationship('User')
    status = db.Column(db.String(40), default='activated')
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<Group (id={self.id}, title={self.title}, ',
            f'owner={self.owner}, status={self.status}, ',
            f'created={self.created})>'
        ])


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User')
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    expires = db.Column(db.DateTime, nullable=True,
                        default=None)

    def __repr__(self):
        return ''.join([
            f'<Session (id={self.id}, user={self.user}, ',
            f'created={self.created}, expires={self.expires})>'
        ])


class Submission(db.Model):
    __bind_key__ = 'scraping'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(40), nullable=True)
    origin = db.Column(db.String(40))
    title = db.Column(db.String(200))
    url = db.Column(db.String(400))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    coordinates = db.relationship('Coordinates')
    fully_scraped = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<Submission (id={self.id}, category={self.category}, ',
            f'origin={self.origin}, title={self.title}, url={self.url}, ',
            f'description={self.description}, price={self.price}, ',
            f'coordinates={self.coordinates}, fully_scraped=',
            f'{self.fully_scraped}, created={self.created})>'
        ])


class CalculatedSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission = db.relationship('Submission')
    group = db.relationship('Group')
    rating = db.Column(db.Integer)
    parameters = db.Column(db.Pickletype)
    status = db.Column(db.String(40))
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<CalculatedSubmission (id={self.id}, submission=',
            f'{self.submission}, group={self.group}, rating={self.rating}, ',
            f'parameters={self.parameters}, status={self.status}, ',
            f'created={self.created})>'
        ])


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.relationship('CalculatedSubmission')
    action = db.Column(db.String(40))
    user = db.relationship('User')
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<Action (id={self.id}, target={self.target}, ',
            f'action={self.action}, user={self.user}, ',
            f'created={self.created})>'
        ])


class Coordinates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    source_latitude = db.Column(db.Integer)
    source_longitude = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<Coordinates (id={self.id}, latitude={self.latitude}, ',
            f'longitude={self.longitude}, created={self.created})>'
        ])


class PairOfCoordinates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.relationship('Coordinates')
    target = db.relationship('Coordinates')
    submission = db.relationship('CalculatedSubmission')
    distance = db.Column(db.Integer)
    time_transit = db.Column(db.Integer)
    time_on_foot = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)
    calculated = db.Column(db.DateTime, nullable=True,
                           default=None)

    def __repr__(self):
        return ''.join([
            f'<PairOfCoordinates (id={self.id}, origin={self.origin}, ',
            f'target={self.target}, calculated={self.calculated}, ',
            f'submission={self.submission}, distance={self.distance}, ',
            f'time_transit={self.time_transit}, time_on_foot=',
            f'{self.time_on_foot}, created={self.created}, calculated=',
            f'{self.calculated})>'
        ])


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(40), default='forbidden')
    center = db.relationship('Coordinates')
    radius = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow)

    def __repr__(self):
        return ''.join([
            f'<Area (id={self.id}, type={self.type}, center={self.center}, ',
            f'radius={self.radius}, created={self.created})>'
        ])

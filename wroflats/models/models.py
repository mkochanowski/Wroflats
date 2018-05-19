from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created = db.Column(db.DateTime, nullable=False, 
        default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    owner = db.relationship('User')
    users = db.relationship('User')
    status = db.Column(db.String(40))
    created = db.Column(db.DateTime, nullable=False, 
        default=datetime.utcnow)

    def __repr__(self):
        return f'<Group {self.users}>'

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User')
    created = db.Column(db.DateTime, nullable=False, 
        default=datetime.utcnow)
    expires = db.Column(db.DateTime, nullable=True, 
        default=Null)

    def __repr__(self):
        return f'<Session {self.user}>'

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(40))
    origin = db.Column(db.String(40))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    coordinates = db.relationship('Coordinates')
    created = db.Column(db.DateTime, nullable=False, 
        default=datetime.utcnow)

    def __repr__(self):
        return f'<Submission {self.id}>'

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
        return f'<CalculatedSubmission {self.id}>'

class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.relationship('CalculatedSubmission')
    action = db.Column(db.String(40))
    user = db.relationship('User')
    created = db.Column(db.DateTime, nullable=False, 
        default=datetime.utcnow)

    def __repr__(self):
        return f'<Action {self.id}>' 

class Coordinates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    calculated = db.Column(db.DateTime, default=False)
    distance = db.Column(db.Integer)
    time_transit = db.Column(db.Integer)
    time_on_foot = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False, 
        default=datetime.utcnow)
    calculated = db.Column(db.DateTime, nullable=True, 
        default=Null)

    def __repr__(self):
        return f'<Coordinates {self.id}%({self.latitude}.{self.longitude})>'


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Kit(db.Model):
    __tablename__ = 'kits'

    id = db.Column(db.Integer, primary_key=True)
    qr_code = db.Column(db.String(100), unique=True, nullable=False)
    activated = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='kit', uselist=False)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    current_level = db.Column(db.Integer, default=1)
    total_score = db.Column(db.Integer, default=0)
    tutorial_completed = db.Column(db.Boolean, default=False)

    kit_id = db.Column(db.Integer, db.ForeignKey('kits.id'))
    kit = db.relationship('Kit', back_populates='user')

    registrations = db.relationship('EventRegistration', back_populates='user')


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.String(50))
    registration_open = db.Column(db.Boolean, default=True)

    registrations = db.relationship('EventRegistration', back_populates='event')


class EventRegistration(db.Model):
    __tablename__ = 'event_registrations'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    user = db.relationship('User', back_populates='registrations')
    event = db.relationship('Event', back_populates='registrations')

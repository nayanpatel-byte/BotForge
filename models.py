from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    tutorial_completed = db.Column(db.Boolean, default=False)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    qr_code = db.Column(db.String(100), unique=True)
    current_level = db.Column(db.Integer, default=1)
    total_score = db.Column(db.Integer, default=0)

class Kit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr_code = db.Column(db.String(100), unique=True)
    activated = db.Column(db.Boolean, default=False)

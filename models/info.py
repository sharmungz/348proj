from . import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    skills = db.relationship('Skill', backref='user', lazy=True)

class Skill(db.Model):
    __tablename__ = 'skills'
    skill_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    skill_name = db.Column(db.String(50), nullable=False, index=True)
    weekly_goal = db.Column(db.Integer, nullable=False)
    activities = db.relationship('Activity', backref='skill', lazy=True)

class Activity(db.Model):
    __tablename__ = 'activities'
    activity_id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    description = db.Column(db.String(200), nullable=True)
    duration = db.Column(db.Integer, nullable=False)  # duration in minutes

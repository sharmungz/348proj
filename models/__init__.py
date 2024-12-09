from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models here for easy access
from models.info import User
from models.info import Skill
from models.info import Activity

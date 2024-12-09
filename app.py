from flask import Flask, render_template
from config import Config
from models import db
from models import User, Skill, Activity  # Import your models from info.py
from routes.skill_routes import skill_bp
from routes.report_routes import report_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def homepage():
    return render_template('homepage.html')

# Register blueprints
app.register_blueprint(skill_bp)
app.register_blueprint(report_bp)

with app.app_context():
    db.create_all()  # This will create the tables in your database if they don’t already exist
    print("Database and tables created!")

def populate_initial_data():
    # Check if data already exists to avoid duplicates
    if not User.query.first():  # Only run if there are no users
        # Create sample users
        user1 = User(username="user1", email="user1@example.com")
        user2 = User(username="user2", email="user2@example.com")
        
        # Add skills for user1
        skill1 = Skill(user_id=1, skill_name="Python Programming", weekly_goal=5)
        skill2 = Skill(user_id=1, skill_name="Data Analysis", weekly_goal=3)
        
        # Create some activities for user1
        activity1 = Activity(user_id=1, skill_id=1, date="2024-10-01", duration=60)
        activity2 = Activity(user_id=1, skill_id=2, date="2024-10-02", duration=90)
        
        # Add all to the session
        db.session.add_all([user1, user2, skill1, skill2, activity1, activity2])
        db.session.commit()
        print("Initial data populated!")
    else:
        print("Data already exists, skipping population.")

"""
# Run this function to populate data
with app.app_context():
    populate_initial_data()
"""

if __name__ == '__main__':
    app.run(debug=True)

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

if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, render_template, request
from sqlalchemy import text
from models import db
from models.info import Skill

report_bp = Blueprint('reports', __name__)

@report_bp.route('/report', methods=['GET', 'POST'])
def report():
    user_id = 1  # Placeholder for logged-in user
    skills = Skill.query.filter_by(user_id=user_id).all()
    activities = []
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        skill_id = request.form['skill_id']
        
        #Prepared statement
        sql = text("""
            SELECT s.skill_name, COUNT(a.activity_id) AS total_activities, SUM(a.duration) AS total_duration
            FROM skills s
            JOIN activities a ON s.skill_id = a.skill_id
            WHERE a.skill_id = :skill_id
            AND a.date BETWEEN :start_date AND :end_date
            GROUP BY s.skill_name
        """)
        
        activities = db.session.execute(sql, {'skill_id': skill_id, 'start_date': start_date, 'end_date': end_date}).fetchall()
    
    return render_template('report.html', skills=skills, activities=activities)

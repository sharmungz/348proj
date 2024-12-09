from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.info import Skill, Activity
from datetime import date, datetime

skill_bp = Blueprint('skills', __name__)

@skill_bp.route('/add_skill', methods=['GET', 'POST'])
def add_skill():
    if request.method == 'POST':
        skill_name = request.form['skill_name']
        weekly_goal = int(request.form['weekly_goal'])
        user_id = 1  # Placeholder for logged-in user
        
        try:
            # Begin a transaction
            db.session.begin()
            new_skill = Skill(user_id=user_id, skill_name=skill_name, weekly_goal=weekly_goal)
            db.session.add(new_skill)
            # Commit the transaction
            db.session.commit()
        except SQLAlchemyError as e:
            # Rollback in case of error
            db.session.rollback()
            # Handle the error (e.g., log it, show a message to the user)
            print(f"Error adding skill: {e}")
        
        return redirect(url_for('skills.list_skills'))
    return render_template('add_skill.html')

@skill_bp.route('/edit_skill/<int:skill_id>', methods=['GET', 'POST'])
def edit_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if request.method == 'POST':
        skill.skill_name = request.form['skill_name']
        skill.weekly_goal = int(request.form['weekly_goal'])
        db.session.commit()
        return redirect(url_for('skills.list_skills'))
    return render_template('edit_skill.html', skill=skill)

@skill_bp.route('/delete_skill/<int:skill_id>', methods=['POST'])
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    return redirect(url_for('skills.list_skills'))

@skill_bp.route('/list_skills')
def list_skills():
    user_id = 1  # Placeholder for logged-in user
    skills = Skill.query.filter_by(user_id=user_id).all()
    return render_template('list_skills.html', skills=skills)

@skill_bp.route('/add_entry/<int:skill_id>', methods=['GET', 'POST'])
def add_entry(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if request.method == 'POST':
        # Convert the date string to a date object
        entry_date_str = request.form.get('date', date.today().isoformat())
        entry_date = datetime.strptime(entry_date_str, '%Y-%m-%d').date()
        
        duration = int(request.form['duration'])
        description = request.form.get('description', '')
        
        # Check if an entry already exists for this skill and date
        existing_entry = Activity.query.filter_by(skill_id=skill_id, date=entry_date).first()
        if existing_entry:
            # Update existing entry
            existing_entry.duration = duration
            existing_entry.description = description
        else:
            # Create new entry
            new_activity = Activity(skill_id=skill_id, date=entry_date, duration=duration, description=description)
            db.session.add(new_activity)
        
        db.session.commit()
        return redirect(url_for('skills.list_skills'))
    
    return render_template('add_entry.html', skill=skill)

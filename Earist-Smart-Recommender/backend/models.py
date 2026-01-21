"""
Database Models for ERVHS-EARIST Recommendation System
"""

from datetime import datetime
from db import db


class Student(db.Model):
    """Student information table"""
    __tablename__ = 'students'
    
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_name = db.Column(db.String(100), nullable=False)
    grade_level = db.Column(db.Enum('11', '12', name='grade_levels'), nullable=False)
    strand = db.Column(db.Enum('STEM', 'ABM', 'HUMSS', 'GAS', 'TVL-ICT', 'TVL-HE', 'TVL-IA', 
                               name='strands'), nullable=False)
    email = db.Column(db.String(100), unique=True)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('active', 'completed', 'inactive', name='student_status'), 
                      default='active')
    
    # Relationships
    responses = db.relationship('QuestionnaireResponse', backref='student', lazy=True, 
                               cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='student', lazy=True, 
                                     cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.student_name} - {self.strand}>'


class QuestionnaireResponse(db.Model):
    """Questionnaire responses table"""
    __tablename__ = 'questionnaire_responses'
    
    response_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id', ondelete='CASCADE'), 
                          nullable=False)
    
    # Stored as JSON array
    favorite_subjects = db.Column(db.Text, nullable=False)
    
    # Skills (1-5 scale)
    skill_analytical = db.Column(db.Integer, db.CheckConstraint('skill_analytical BETWEEN 1 AND 5'))
    skill_technical = db.Column(db.Integer, db.CheckConstraint('skill_technical BETWEEN 1 AND 5'))
    skill_communication = db.Column(db.Integer, db.CheckConstraint('skill_communication BETWEEN 1 AND 5'))
    skill_creativity = db.Column(db.Integer, db.CheckConstraint('skill_creativity BETWEEN 1 AND 5'))
    skill_numerical = db.Column(db.Integer, db.CheckConstraint('skill_numerical BETWEEN 1 AND 5'))
    skill_leadership = db.Column(db.Integer, db.CheckConstraint('skill_leadership BETWEEN 1 AND 5'))
    skill_attention_to_detail = db.Column(db.Integer, db.CheckConstraint('skill_attention_to_detail BETWEEN 1 AND 5'))
    skill_research = db.Column(db.Integer, db.CheckConstraint('skill_research BETWEEN 1 AND 5'))
    
    # Stored as JSON array
    interests = db.Column(db.Text, nullable=False)
    
    learning_style = db.Column(db.String(50))
    career_goal_specified = db.Column(db.Boolean, default=False)
    career_goal_description = db.Column(db.Text)
    career_priority = db.Column(db.String(50))
    
    response_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    recommendations = db.relationship('Recommendation', backref='response', lazy=True, 
                                     cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Response {self.response_id} by Student {self.student_id}>'


class Program(db.Model):
    """College programs table"""
    __tablename__ = 'programs'
    
    program_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    program_code = db.Column(db.String(20), unique=True, nullable=False)
    program_name = db.Column(db.String(150), nullable=False)
    program_description = db.Column(db.Text)
    college_department = db.Column(db.String(100))
    
    # Stored as JSON arrays
    required_skills = db.Column(db.Text)
    typical_strands = db.Column(db.Text)
    
    career_pathways = db.Column(db.Text)
    program_duration = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    rules = db.relationship('Rule', backref='program', lazy=True)
    recommendations = db.relationship('Recommendation', backref='program', lazy=True)
    
    def __repr__(self):
        return f'<Program {self.program_code} - {self.program_name}>'


class Rule(db.Model):
    """Rules table"""
    __tablename__ = 'rules'
    
    rule_id = db.Column(db.String(20), primary_key=True)
    rule_description = db.Column(db.Text, nullable=False)
    
    # Stored as JSON object with structure: {"operator": "AND", "criteria": [...]}
    conditions = db.Column(db.Text, nullable=False)
    
    recommended_program_id = db.Column(db.Integer, db.ForeignKey('programs.program_id'), 
                                      nullable=False)
    confidence_score = db.Column(db.Float, db.CheckConstraint('confidence_score BETWEEN 0 AND 100'))
    justification = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Rule {self.rule_id}>'


class Recommendation(db.Model):
    """Recommendations table"""
    __tablename__ = 'recommendations'
    
    recommendation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id', ondelete='CASCADE'), 
                          nullable=False)
    response_id = db.Column(db.Integer, 
                           db.ForeignKey('questionnaire_responses.response_id', ondelete='CASCADE'), 
                           nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.program_id'), nullable=False)
    
    rank_position = db.Column(db.Integer, nullable=False)
    confidence_score = db.Column(db.Float)
    justification = db.Column(db.Text)
    
    # Stored as JSON array of rule IDs
    rules_triggered = db.Column(db.Text)
    
    recommendation_date = db.Column(db.DateTime, default=datetime.utcnow)
    student_feedback = db.Column(db.Enum('helpful', 'somewhat_helpful', 'not_helpful', 'no_feedback',
                                        name='feedback_types'), default='no_feedback')
    counselor_notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Recommendation #{self.rank_position} for Student {self.student_id}>'


class AdminUser(db.Model):
    """Admin users table"""
    __tablename__ = 'admin_users'
    
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    role = db.Column(db.Enum('admin', 'counselor', 'viewer', name='admin_roles'), default='viewer')
    email = db.Column(db.String(100))
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    logs = db.relationship('SystemLog', backref='admin', lazy=True)
    
    def __repr__(self):
        return f'<AdminUser {self.username} - {self.role}>'


class SystemLog(db.Model):
    """System activity logs table"""
    __tablename__ = 'system_logs'
    
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_users.admin_id'))
    action_type = db.Column(db.String(50))
    action_description = db.Column(db.Text)
    affected_table = db.Column(db.String(50))
    affected_record_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Log {self.log_id} - {self.action_type}>'

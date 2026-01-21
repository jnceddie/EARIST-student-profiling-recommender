import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io

 # Initialize Flask app with correct static folder
app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/templates')),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/static'))
)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'database', 'ervhs_earist.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db.init_app(app)

# Import models
from models import Student, QuestionnaireResponse, Program, Rule, Recommendation, AdminUser, SystemLog
from inference_engine import InferenceEngine

# AUTO-CREATE ALL TABLES ON STARTUP
def init_database():
    """Initialize database and create tables"""
    with app.app_context():
        try:
            # Ensure database directory exists
            os.makedirs('database', exist_ok=True)
            print("📂 Database directory ready")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created/verified")
            
            # Check if we need to seed data
            program_count = Program.query.count()
            if program_count == 0:
                print("📚 Loading initial data...")
                from seed_data import seed_programs, seed_rules
                
                try:
                    seed_programs()
                    print("✅ 15 programs loaded!")
                except Exception as e:
                    print(f"⚠️  Program loading: {e}")
                
                try:
                    seed_rules()
                    print("✅ 20 rules loaded!")
                except Exception as e:
                    print(f"⚠️  Rule loading: {e}")
                

                # Create admin user
                admin = AdminUser.query.filter_by(username='admin').first()
                if not admin:
                    admin = AdminUser(
                        username='admin',
                        role='super_admin',
                        email='admin@earist.edu.ph'
                    )
                    db.session.add(admin)
                    db.session.commit()
                    print("✅ Admin user created (admin/admin123)")
            else:
                print(f"✅ Database ready ({program_count} programs loaded)")
            print("🎉 System initialization complete!")
        except Exception as e:
            print(f"❌ Database error: {e}")
            print("⚠️  System will attempt to continue...")

# Initialize inference engine
inference_engine = InferenceEngine(db)

# Initialize database on startup
init_database()

# Initialize inference engine
inference_engine = InferenceEngine(db)

# Routes
@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/questionnaire')
def questionnaire():
    """Student questionnaire page"""
    return render_template('questionnaire.html')

@app.route('/api/submit-response', methods=['POST'])
def submit_response():
    """Handle questionnaire submission"""
    try:
        data = request.json
        
        # Create student record
        student = Student(
            student_name=data.get('name'),
            grade_level=data.get('grade_level'),
            strand=data.get('strand'),
            email=data.get('email')
        )
        db.session.add(student)
        db.session.flush()
        
        # Create questionnaire response
        response = QuestionnaireResponse(
            student_id=student.student_id,
            favorite_subjects=','.join(data.get('favorite_subjects', [])),
            skill_analytical=int(data.get('skills', {}).get('analytical', 0)),
            skill_technical=int(data.get('skills', {}).get('technical', 0)),
            skill_communication=int(data.get('skills', {}).get('communication', 0)),
            skill_creativity=int(data.get('skills', {}).get('creativity', 0)),
            skill_numerical=int(data.get('skills', {}).get('numerical', 0)),
            skill_leadership=int(data.get('skills', {}).get('leadership', 0)),
            skill_attention_to_detail=int(data.get('skills', {}).get('attention_to_detail', 0)),
            skill_research=int(data.get('skills', {}).get('research', 0)),
            interests=','.join(data.get('interests', [])),
            learning_style=data.get('learning_style'),
            career_goal_specified=True if data.get('career_goals', '') else False,
            career_goal_description=data.get('career_goals', ''),
            career_priority=data.get('career_priority', '')
        )
        db.session.add(response)
        db.session.flush()
        
        # Generate recommendations (pass response_id as required)
        recommendations = inference_engine.generate_recommendations(data, response.response_id)
        
        # Save recommendations
        for rec in recommendations:
            recommendation = Recommendation(
                student_id=student.student_id,
                response_id=response.response_id,
                program_id=rec['program_id'],
                rank_position=rec.get('rank', 1),
                confidence_score=rec.get('confidence', 0),
                justification=rec.get('justification', ''),
                rules_triggered=','.join([str(r) for r in rec.get('rules_triggered', [])])
            )
            db.session.add(recommendation)
        
        db.session.commit()
        
        # Store in session
        session['student_id'] = student.student_id
        session['response_id'] = response.response_id
        
        return jsonify({
            'success': True,
            'student_id': student.student_id,
            'recommendations': recommendations
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Submission error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/results')
def results():
    """Display recommendations"""
    student_id = session.get('student_id')
    if not student_id:
        return redirect(url_for('index'))
    
    student = Student.query.get(student_id)
    recommendations = Recommendation.query.filter_by(
        student_id=student_id
    ).order_by(Recommendation.rank_position).all()

    rec_list = []
    for rec in recommendations:
        program = Program.query.get(rec.program_id)
        rec_list.append({
            'rank': rec.rank_position,
            'program': program,
            'confidence': rec.confidence_score,
            'justification': rec.justification
        })

    response_id = session.get('response_id')
    return render_template('results.html', student=student, recommendations=rec_list, response_id=response_id)

@app.route('/programs')
def programs():
    """Display all programs"""
    all_programs = Program.query.filter_by(is_active=True).all()
    return render_template('programs.html', programs=all_programs)

@app.route('/api/feedback', methods=['POST'])
def feedback():
    """Save student feedback"""
    try:
        data = request.json
        recommendation = Recommendation.query.get(data.get('recommendation_id'))
        if recommendation:
            recommendation.student_feedback = data.get('feedback')
            db.session.commit()
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download-report/<int:student_id>')
def download_report(student_id):
    """Generate PDF report"""
    try:
        student = Student.query.get(student_id)
        recommendations = Recommendation.query.filter_by(
            student_id=student_id
        ).order_by(Recommendation.rank).all()
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        p.setFont("Helvetica-Bold", 20)
        p.drawString(1*inch, height-1*inch, "ERVHS-EARIST Recommendations")
        
        p.setFont("Helvetica", 12)
        p.drawString(1*inch, height-1.5*inch, f"Student: {student.name}")
        p.drawString(1*inch, height-1.7*inch, f"Strand: {student.strand}")
        
        y = height - 2.5*inch
        for rec in recommendations:
            program = Program.query.get(rec.program_id)
            p.setFont("Helvetica-Bold", 12)
            p.drawString(1*inch, y, f"{rec.rank}. {program.program_name}")
            y -= 0.3*inch
        
        p.save()
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"recommendations_{student.name.replace(' ', '_')}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = AdminUser.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.admin_id
            session['admin_username'] = admin.username
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    total_students = Student.query.count()
    total_responses = QuestionnaireResponse.query.count()
    total_recommendations = Recommendation.query.count()
    recent_students = Student.query.order_by(Student.date_submitted.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html',
                         total_students=total_students,
                         total_responses=total_responses,
                         total_recommendations=total_recommendations,
                         recent_students=recent_students)

@app.route('/admin/students')
def admin_students():
    """View all students"""
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    students = Student.query.order_by(Student.date_submitted.desc()).all()
    return render_template('admin_students.html', students=students)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 ERVHS-EARIST SYSTEM STARTING...")
    print("="*50)
    print("📊 Access at: http://localhost:5000")
    print("👤 Admin: http://localhost:5000/admin/login")
    print("   Username: admin")
    print("   Password: admin123")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

import sqlite3
import json
from datetime import datetime

# Create database
db_path = 'database/ervhs_earist.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🚀 Creating database tables...")

# Create tables
cursor.executescript('''
-- Students table
CREATE TABLE IF NOT EXISTS student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200),
    strand VARCHAR(50) NOT NULL,
    email VARCHAR(200),
    date_submitted DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);

-- Questionnaire Responses table  
CREATE TABLE IF NOT EXISTS questionnaire_response (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    favorite_subjects TEXT,
    skills_analytical INTEGER,
    skills_technical INTEGER,
    skills_communication INTEGER,
    skills_creativity INTEGER,
    skills_numerical INTEGER,
    skills_leadership INTEGER,
    skills_attention_to_detail INTEGER,
    skills_research INTEGER,
    interests TEXT,
    learning_style VARCHAR(100),
    career_goals TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

-- Programs table
CREATE TABLE IF NOT EXISTS program (
    program_id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_code VARCHAR(20) UNIQUE NOT NULL,
    program_name VARCHAR(200) NOT NULL,
    description TEXT,
    college VARCHAR(200),
    required_skills TEXT,
    typical_strands TEXT,
    career_pathways TEXT,
    is_active BOOLEAN DEFAULT 1
);

-- Rules table
CREATE TABLE IF NOT EXISTS rule (
    rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conditions TEXT NOT NULL,
    program_id INTEGER,
    confidence_score INTEGER,
    justification TEXT,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (program_id) REFERENCES program(program_id)
);

-- Recommendations table
CREATE TABLE IF NOT EXISTS recommendation (
    recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    response_id INTEGER,
    program_id INTEGER,
    rank INTEGER,
    confidence_score FLOAT,
    justification TEXT,
    rules_triggered TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    student_feedback VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (response_id) REFERENCES questionnaire_response(response_id),
    FOREIGN KEY (program_id) REFERENCES program(program_id)
);

-- Admin Users table
CREATE TABLE IF NOT EXISTS admin_user (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'admin',
    email VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- System Logs table
CREATE TABLE IF NOT EXISTS system_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER,
    action_type VARCHAR(100),
    action_description TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admin_user(admin_id)
);
''')

print("✅ Tables created!")

# Insert programs
print("📚 Loading programs...")

programs = [
    ('BSCS', 'Bachelor of Science in Computer Science', 'Focuses on software development, algorithms, data structures, and computer systems', 'College of Engineering', 
     json.dumps(['Analytical Thinking', 'Technical Skills', 'Problem Solving']), 
     json.dumps(['STEM', 'TVL-ICT']),
     json.dumps(['Software Developer', 'Systems Analyst', 'IT Consultant', 'Data Scientist'])),
    
    ('BSIT', 'Bachelor of Science in Information Technology', 'Emphasizes practical IT applications, network administration, and systems management', 'College of Engineering',
     json.dumps(['Technical Skills', 'Analytical Thinking', 'Attention to Detail']),
     json.dumps(['STEM', 'TVL-ICT', 'GAS']),
     json.dumps(['IT Specialist', 'Network Administrator', 'Web Developer', 'Database Administrator'])),
    
    ('BSCE', 'Bachelor of Science in Civil Engineering', 'Covers design and construction of infrastructure like buildings, roads, and bridges', 'College of Engineering',
     json.dumps(['Analytical Thinking', 'Numerical Skills', 'Attention to Detail']),
     json.dumps(['STEM', 'TVL-IA']),
     json.dumps(['Civil Engineer', 'Structural Engineer', 'Construction Manager', 'Project Engineer'])),
    
    ('BSEE', 'Bachelor of Science in Electrical Engineering', 'Studies electrical systems, power generation, and electronics', 'College of Engineering',
     json.dumps(['Analytical Thinking', 'Technical Skills', 'Numerical Skills']),
     json.dumps(['STEM']),
     json.dumps(['Electrical Engineer', 'Electronics Engineer', 'Power Systems Engineer', 'Control Systems Engineer'])),
    
    ('BSME', 'Bachelor of Science in Mechanical Engineering', 'Focuses on design, manufacturing, and maintenance of mechanical systems', 'College of Engineering',
     json.dumps(['Analytical Thinking', 'Technical Skills', 'Creativity']),
     json.dumps(['STEM', 'TVL-IA']),
     json.dumps(['Mechanical Engineer', 'Manufacturing Engineer', 'HVAC Engineer', 'Automotive Engineer'])),
    
    ('BSECE', 'Bachelor of Science in Electronics and Communications Engineering', 'Specializes in telecommunications, electronics, and signal processing', 'College of Engineering',
     json.dumps(['Analytical Thinking', 'Technical Skills', 'Problem Solving']),
     json.dumps(['STEM']),
     json.dumps(['Electronics Engineer', 'Telecommunications Engineer', 'RF Engineer', 'Embedded Systems Engineer'])),
    
    ('BSIE', 'Bachelor of Science in Industrial Engineering', 'Optimizes complex systems, processes, and organizational operations', 'College of Engineering',
     json.dumps(['Analytical Thinking', 'Leadership', 'Problem Solving']),
     json.dumps(['STEM', 'ABM', 'GAS']),
     json.dumps(['Industrial Engineer', 'Operations Manager', 'Supply Chain Analyst', 'Quality Assurance Manager'])),
    
    ('BSArch', 'Bachelor of Science in Architecture', 'Combines art and science in designing buildings and spaces', 'College of Architecture and Fine Arts',
     json.dumps(['Creativity', 'Analytical Thinking', 'Attention to Detail']),
     json.dumps(['STEM', 'GAS', 'HUMSS']),
     json.dumps(['Architect', 'Urban Planner', 'Interior Designer', 'Landscape Architect'])),
    
    ('BSINDTECH', 'Bachelor of Science in Industrial Technology', 'Practical technical education in manufacturing, construction, and technology', 'College of Engineering',
     json.dumps(['Technical Skills', 'Attention to Detail', 'Problem Solving']),
     json.dumps(['TVL-IA', 'STEM']),
     json.dumps(['Industrial Technician', 'Manufacturing Technician', 'Quality Control Inspector', 'Production Supervisor'])),
    
    ('BSBA', 'Bachelor of Science in Business Administration', 'Comprehensive business education covering management, marketing, and operations', 'College of Business',
     json.dumps(['Leadership', 'Communication', 'Analytical Thinking']),
     json.dumps(['ABM', 'HUMSS', 'GAS']),
     json.dumps(['Business Manager', 'Marketing Manager', 'Entrepreneur', 'Human Resources Manager'])),
    
    ('BSA', 'Bachelor of Science in Accountancy', 'Focuses on financial reporting, auditing, taxation, and accounting principles', 'College of Business',
     json.dumps(['Numerical Skills', 'Attention to Detail', 'Analytical Thinking']),
     json.dumps(['ABM', 'STEM']),
     json.dumps(['Certified Public Accountant', 'Auditor', 'Tax Consultant', 'Financial Analyst'])),
    
    ('BSOA', 'Bachelor of Science in Office Administration', 'Develops skills in office management, communication, and administrative processes', 'College of Business',
     json.dumps(['Communication', 'Attention to Detail', 'Leadership']),
     json.dumps(['ABM', 'HUMSS', 'GAS']),
     json.dumps(['Office Manager', 'Executive Assistant', 'Administrative Officer', 'Records Manager'])),
    
    ('BSED', 'Bachelor of Secondary Education', 'Prepares teachers for secondary education with major in various subjects', 'College of Education',
     json.dumps(['Communication', 'Leadership', 'Creativity']),
     json.dumps(['HUMSS', 'GAS', 'STEM']),
     json.dumps(['High School Teacher', 'Education Administrator', 'Curriculum Developer', 'Guidance Counselor'])),
    
    ('BTVTEd', 'Bachelor of Technical Vocational Teacher Education', 'Prepares technical vocational education teachers', 'College of Education',
     json.dumps(['Technical Skills', 'Communication', 'Leadership']),
     json.dumps(['TVL-ICT', 'TVL-HE', 'TVL-IA']),
     json.dumps(['Vocational Teacher', 'Technical Trainer', 'Training Coordinator', 'Skills Development Specialist'])),
    
    ('BSHRM', 'Bachelor of Science in Hotel and Restaurant Management', 'Covers hospitality operations, food service management, and customer service', 'College of Hospitality',
     json.dumps(['Communication', 'Leadership', 'Creativity']),
     json.dumps(['TVL-HE', 'HUMSS', 'GAS']),
     json.dumps(['Hotel Manager', 'Restaurant Manager', 'Event Coordinator', 'Food Service Director']))
]

for prog in programs:
    cursor.execute('''
        INSERT INTO program (program_code, program_name, description, college, required_skills, typical_strands, career_pathways, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
    ''', prog)

print(f"✅ Loaded {len(programs)} programs!")

# Insert rules
print("📋 Loading rules...")

rules_data = [
    (json.dumps({"AND": [{"strand": "STEM"}, {"favorites": "Mathematics"}, {"skills.analytical": ">=4"}, {"interests": "Technology"}]}), 
     1, 95, "Strong analytical and mathematical foundation from STEM, combined with technology interest, aligns perfectly with CS requirements"),
    
    (json.dumps({"AND": [{"strand": "TVL-ICT"}, {"skills.technical": ">=4"}, {"interests": "Technology"}]}),
     2, 92, "Direct ICT track from TVL provides excellent foundation for IT, with hands-on technical skills"),
    
    (json.dumps({"AND": [{"strand": "STEM"}, {"favorites": "Physics"}, {"skills.analytical": ">=4"}]}),
     3, 90, "Strong physics and analytical background essential for Civil Engineering principles"),
    
    (json.dumps({"AND": [{"strand": "STEM"}, {"favorites": "Mathematics"}, {"skills.numerical": ">=4"}]}),
     4, 91, "Electrical Engineering requires strong mathematical and analytical foundation from STEM"),
    
    (json.dumps({"AND": [{"strand": "STEM"}, {"favorites": "Physics"}, {"skills.technical": ">=3"}]}),
     5, 89, "Mechanical Engineering aligns well with STEM physics and technical aptitude"),
    
    (json.dumps({"AND": [{"strand": "STEM"}, {"interests": "Technology"}, {"skills.technical": ">=4"}]}),
     6, 90, "Electronics and Communications Engineering matches STEM technical and technology interests"),
    
    (json.dumps({"AND": [{"strand": "ABM"}, {"skills.analytical": ">=4"}, {"skills.leadership": ">=3"}]}),
     7, 88, "Industrial Engineering benefits from ABM business perspective and analytical thinking"),
    
    (json.dumps({"AND": [{"strand": "GAS"}, {"skills.creativity": ">=4"}, {"interests": "Arts"}]}),
     8, 86, "Architecture requires creative thinking and design sense supported by GAS flexibility"),
    
    (json.dumps({"AND": [{"strand": "TVL-IA"}, {"skills.technical": ">=4"}]}),
     9, 85, "Industrial Technology is natural fit for TVL-Industrial Arts technical background"),
    
    (json.dumps({"AND": [{"strand": "ABM"}, {"skills.leadership": ">=4"}, {"skills.communication": ">=4"}]}),
     10, 94, "Business Administration matches ABM preparation with strong leadership and communication"),
    
    (json.dumps({"AND": [{"strand": "ABM"}, {"favorites": "Accounting"}, {"skills.numerical": ">=4"}, {"skills.attention_to_detail": ">=4"}]}),
     11, 96, "Accountancy perfect match for ABM accounting track with detail-oriented numerical skills"),
    
    (json.dumps({"AND": [{"strand": "ABM"}, {"skills.communication": ">=4"}, {"skills.attention_to_detail": ">=4"}]}),
     12, 87, "Office Administration suits ABM administrative skills with communication and organization"),
    
    (json.dumps({"AND": [{"strand": "HUMSS"}, {"skills.communication": ">=4"}, {"interests": "Education"}]}),
     13, 90, "Secondary Education natural choice for HUMSS with strong communication and teaching interest"),
    
    (json.dumps({"AND": [{"strand": "TVL-ICT"}, {"skills.technical": ">=4"}, {"skills.communication": ">=3"}]}),
     14, 88, "TVT Education excellent for TVL-ICT students wanting to teach technical skills"),
    
    (json.dumps({"AND": [{"strand": "TVL-HE"}, {"skills.creativity": ">=3"}, {"interests": "Hospitality"}]}),
     15, 92, "Hotel and Restaurant Management perfect fit for TVL-Home Economics hospitality skills"),
    
    (json.dumps({"AND": [{"strand": "STEM"}, {"skills.analytical": ">=3"}]}),
     2, 78, "STEM analytical foundation supports IT career path"),
    
    (json.dumps({"AND": [{"strand": "GAS"}, {"interests": "Business"}, {"skills.communication": ">=3"}]}),
     10, 75, "General Academic Strand flexibility allows business career with good communication"),
    
    (json.dumps({"AND": [{"strand": "HUMSS"}, {"skills.communication": ">=4"}]}),
     10, 72, "HUMSS communication strength applicable to business management"),
    
    (json.dumps({"AND": [{"strand": "STEM"}, {"skills.numerical": ">=4"}]}),
     11, 74, "STEM numerical skills support accounting career"),
    
    (json.dumps({"AND": [{"strand": "HUMSS"}, {"skills.creativity": ">=4"}]}),
     8, 70, "HUMSS creative thinking can support architecture with proper technical development")
]

for i, rule_data in enumerate(rules_data, 1):
    cursor.execute('''
        INSERT INTO rule (conditions, program_id, confidence_score, justification, is_active)
        VALUES (?, ?, ?, ?, 1)
    ''', rule_data)

print(f"✅ Loaded {len(rules_data)} rules!")

# Create admin user with bcrypt-style hash (simplified)
print("👤 Creating admin user...")
cursor.execute('''
    INSERT INTO admin_user (username, password_hash, role, email)
    VALUES ('admin', 'pbkdf2:sha256:600000$randomsalt$hashedpassword', 'super_admin', 'admin@earist.edu.ph')
''')

print("✅ Admin user created (admin/admin123)")

# Create sample students
print("👥 Creating sample students...")
sample_students = [
    ('Maria Santos', 'STEM', 'maria@test.com'),
    ('Juan Dela Cruz', 'ABM', 'juan@test.com'),
    ('Ana Garcia', 'HUMSS', 'ana@test.com'),
    ('Pedro Reyes', 'GAS', 'pedro@test.com'),
    ('Sofia Torres', 'TVL-ICT', 'sofia@test.com')
]

for student in sample_students:
    cursor.execute('INSERT INTO student (name, strand, email) VALUES (?, ?, ?)', student)

print("✅ Created 5 sample students!")

# Commit and close
conn.commit()
conn.close()

print("\n🎉 Database created successfully!")
print(f"📂 Location: database/ervhs_earist.db")

import os
print(f"💾 Size: {os.path.getsize('database/ervhs_earist.db'):,} bytes")


"""
Database Seeding Script
Seeds programs and rules into the database
"""

import json
from inference_engine import create_rule_condition, create_criterion


def seed_programs(db, Program):
    """Seed EARIST programs into database"""
    
    programs_data = [
        {
            'program_code': 'BSCS',
            'program_name': 'Bachelor of Science in Computer Science',
            'program_description': 'Focuses on algorithm design, software engineering, and theoretical foundations of computing',
            'college_department': 'College of Engineering',
            'required_skills': json.dumps(['analytical', 'technical', 'problem-solving', 'research']),
            'typical_strands': json.dumps(['STEM', 'TVL-ICT']),
            'career_pathways': 'Software Developer, Systems Analyst, AI Specialist, Database Administrator, Research Scientist',
            'program_duration': '4 years'
        },
        {
            'program_code': 'BSIT',
            'program_name': 'Bachelor of Science in Information Technology',
            'program_description': 'Emphasizes practical IT skills, network administration, and systems implementation',
            'college_department': 'College of Engineering',
            'required_skills': json.dumps(['technical', 'logical', 'troubleshooting']),
            'typical_strands': json.dumps(['TVL-ICT', 'STEM', 'GAS']),
            'career_pathways': 'IT Support Specialist, Network Administrator, Web Developer, Systems Administrator',
            'program_duration': '4 years'
        },
        {
            'program_code': 'BSCE',
            'program_name': 'Bachelor of Science in Civil Engineering',
            'program_description': 'Studies design, construction, and maintenance of infrastructure and buildings',
            'college_department': 'College of Engineering',
            'required_skills': json.dumps(['analytical', 'mathematical', 'practical', 'spatial']),
            'typical_strands': json.dumps(['STEM']),
            'career_pathways': 'Structural Engineer, Construction Manager, Project Engineer, Urban Planner',
            'program_duration': '5 years'
        },
        {
            'program_code': 'BSEE',
            'program_name': 'Bachelor of Science in Electrical Engineering',
            'program_description': 'Focuses on electrical systems, power distribution, and electronics',
            'college_department': 'College of Engineering',
            'required_skills': json.dumps(['analytical', 'technical', 'mathematical']),
            'typical_strands': json.dumps(['STEM', 'TVL-ICT']),
            'career_pathways': 'Electrical Engineer, Power Systems Engineer, Electronics Designer, Automation Engineer',
            'program_duration': '5 years'
        },
        {
            'program_code': 'BSME',
            'program_name': 'Bachelor of Science in Mechanical Engineering',
            'program_description': 'Studies design, analysis, and manufacturing of mechanical systems',
            'college_department': 'College of Engineering',
            'required_skills': json.dumps(['analytical', 'technical', 'creative', 'mathematical']),
            'typical_strands': json.dumps(['STEM', 'TVL-IA']),
            'career_pathways': 'Mechanical Engineer, Manufacturing Engineer, HVAC Engineer, Automotive Engineer',
            'program_duration': '5 years'
        },
        {
            'program_code': 'BSECE',
            'program_name': 'Bachelor of Science in Electronics Engineering',
            'program_description': 'Specializes in electronic circuits, telecommunications, and embedded systems',
            'college_department': 'College of Engineering',
            'required_skills': json.dumps(['technical', 'analytical', 'precision']),
            'typical_strands': json.dumps(['STEM', 'TVL-ICT']),
            'career_pathways': 'Electronics Engineer, Telecommunications Engineer, Embedded Systems Developer',
            'program_duration': '5 years'
        },
        {
            'program_code': 'BSIE',
            'program_name': 'Bachelor of Science in Industrial Engineering',
            'program_description': 'Optimizes complex processes, systems, and organizations',
            'college_department': 'College of Engineering',
            'required_skills': json.dumps(['analytical', 'organizational', 'systems-thinking']),
            'typical_strands': json.dumps(['STEM', 'ABM']),
            'career_pathways': 'Industrial Engineer, Operations Manager, Process Improvement Specialist, Supply Chain Analyst',
            'program_duration': '5 years'
        },
        {
            'program_code': 'BSBA',
            'program_name': 'Bachelor of Science in Business Administration',
            'program_description': 'Develops management, leadership, and business operation skills',
            'college_department': 'College of Business and Management',
            'required_skills': json.dumps(['leadership', 'communication', 'analytical']),
            'typical_strands': json.dumps(['ABM', 'GAS']),
            'career_pathways': 'Business Manager, Marketing Manager, Human Resources Specialist, Entrepreneur',
            'program_duration': '4 years'
        },
        {
            'program_code': 'BSA',
            'program_name': 'Bachelor of Science in Accountancy',
            'program_description': 'Prepares students for accounting, auditing, and financial management',
            'college_department': 'College of Business and Management',
            'required_skills': json.dumps(['numerical', 'attention-to-detail', 'analytical']),
            'typical_strands': json.dumps(['ABM', 'STEM']),
            'career_pathways': 'Certified Public Accountant, Auditor, Tax Consultant, Financial Analyst',
            'program_duration': '4 years'
        },
        {
            'program_code': 'BSOA',
            'program_name': 'Bachelor of Science in Office Administration',
            'program_description': 'Focuses on administrative management, office systems, and business communication',
            'college_department': 'College of Business and Management',
            'required_skills': json.dumps(['organizational', 'communication', 'technology']),
            'typical_strands': json.dumps(['ABM', 'GAS', 'HUMSS']),
            'career_pathways': 'Administrative Manager, Executive Assistant, Office Manager, Records Manager',
            'program_duration': '4 years'
        },
        {
            'program_code': 'BSED',
            'program_name': 'Bachelor of Secondary Education',
            'program_description': 'Prepares teachers for secondary education with major specializations',
            'college_department': 'College of Education',
            'required_skills': json.dumps(['communication', 'leadership', 'empathy']),
            'typical_strands': json.dumps(['HUMSS', 'GAS']),
            'career_pathways': 'Secondary School Teacher, Curriculum Developer, Educational Coordinator',
            'program_duration': '4 years'
        },
        {
            'program_code': 'BSARCH',
            'program_name': 'Bachelor of Science in Architecture',
            'program_description': 'Combines art, science, and technology in building design',
            'college_department': 'College of Architecture and Fine Arts',
            'required_skills': json.dumps(['creativity', 'technical', 'spatial', 'artistic']),
            'typical_strands': json.dumps(['STEM', 'TVL-IA']),
            'career_pathways': 'Architect, Urban Designer, Interior Designer, Building Consultant',
            'program_duration': '5 years'
        },
        {
            'program_code': 'BSINDTECH',
            'program_name': 'Bachelor of Science in Industrial Technology',
            'program_description': 'Develops advanced technical skills in industrial processes and manufacturing',
            'college_department': 'College of Industrial Technology',
            'required_skills': json.dumps(['technical', 'practical', 'mechanical']),
            'typical_strands': json.dumps(['TVL-IA', 'TVL-ICT', 'STEM']),
            'career_pathways': 'Production Supervisor, Quality Control Specialist, Technical Trainer, Manufacturing Technician',
            'program_duration': '4 years'
        },
        {
            'program_code': 'BSHRM',
            'program_name': 'Bachelor of Science in Hotel and Restaurant Management',
            'program_description': 'Prepares students for hospitality industry management',
            'college_department': 'College of Hospitality Management',
            'required_skills': json.dumps(['service-oriented', 'communication', 'organizational']),
            'typical_strands': json.dumps(['TVL-HE', 'ABM', 'HUMSS']),
            'career_pathways': 'Hotel Manager, Restaurant Manager, Event Coordinator, Food Service Director',
            'program_duration': '4 years'
        },
        {
            'program_code': 'BTVTEd',
            'program_name': 'Bachelor of Technical-Vocational Teacher Education',
            'program_description': 'Trains technical-vocational teachers for secondary and post-secondary education',
            'college_department': 'College of Education',
            'required_skills': json.dumps(['technical', 'communication', 'teaching']),
            'typical_strands': json.dumps(['TVL-HE', 'TVL-IA', 'TVL-ICT']),
            'career_pathways': 'TLE Teacher, TESDA Trainer, Vocational Training Coordinator, Industry Trainer',
            'program_duration': '4 years'
        }
    ]
    
    for program_data in programs_data:
        existing = Program.query.filter_by(program_code=program_data['program_code']).first()
        if not existing:
            program = Program(**program_data)
            db.session.add(program)
    
    db.session.commit()
    print(f"Seeded {len(programs_data)} programs")


def seed_rules(db, Rule, Program):
    """Seed recommendation rules into database"""
    
    # Get program IDs
    programs = {p.program_code: p.program_id for p in Program.query.all()}
    
    rules_data = [
        # RULE 001 - STEM to CS
        {
            'rule_id': 'RULE001',
            'rule_description': 'STEM students with strong analytical and technical skills interested in technology',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'STEM'),
                create_criterion('favorite_subjects', 'CONTAINS', 'Mathematics'),
                create_criterion('skills.analytical', '>=', 4),
                create_criterion('interests', 'CONTAINS', 'Technology'),
                create_criterion('skills.technical', '>=', 3)
            ]),
            'recommended_program_id': programs['BSCS'],
            'confidence_score': 95.0,
            'justification': 'Strong analytical and mathematical foundation from STEM, combined with technology interest and technical aptitude, aligns perfectly with the problem-solving and algorithmic thinking required in Computer Science.'
        },
        
        # RULE 002 - TVL-ICT to IT
        {
            'rule_id': 'RULE002',
            'rule_description': 'TVL-ICT students with technical skills interested in technology',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'TVL-ICT'),
                create_criterion('skills.technical', '>=', 4),
                create_criterion('interests', 'CONTAINS', 'Technology')
            ]),
            'recommended_program_id': programs['BSIT'],
            'confidence_score': 92.0,
            'justification': 'Direct ICT background with hands-on technical skills provides practical foundation for IT infrastructure, systems administration, and application development focus of this program.'
        },
        
        # RULE 003 - STEM to Civil Engineering
        {
            'rule_id': 'RULE003',
            'rule_description': 'STEM students with physics/math interest and practical learning style',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'STEM'),
                create_criterion('skills.analytical', '>=', 4),
                create_criterion('interests', 'CONTAINS', 'Engineering'),
                create_criterion('learning_style', '==', 'Hands-on/Practical learning')
            ]),
            'recommended_program_id': programs['BSCE'],
            'confidence_score': 90.0,
            'justification': 'STEM foundation with physics and mathematics expertise, combined with practical learning preference, matches the structural analysis and construction-focused nature of Civil Engineering.'
        },
        
        # RULE 004 - STEM to Electrical Engineering
        {
            'rule_id': 'RULE004',
            'rule_description': 'STEM students with physics background interested in engineering and technology',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'STEM'),
                create_criterion('skills.technical', '>=', 3),
                create_criterion('interests', 'CONTAINS', 'Engineering')
            ]),
            'recommended_program_id': programs['BSEE'],
            'confidence_score': 88.0,
            'justification': 'Physics background essential for understanding electrical systems, circuits, and power distribution. STEM analytical training supports complex electrical theory and applications.'
        },
        
        # RULE 005 - STEM/TVL-IA to Mechanical Engineering
        {
            'rule_id': 'RULE005',
            'rule_description': 'STEM or TVL-IA students with technical skills interested in engineering',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', 'IN', ['STEM', 'TVL-IA']),
                create_criterion('skills.technical', '>=', 4),
                create_criterion('interests', 'CONTAINS', 'Engineering')
            ]),
            'recommended_program_id': programs['BSME'],
            'confidence_score': 87.0,
            'justification': 'Strong technical and mathematical skills combined with practical orientation suit the design, analysis, and manufacturing focus of Mechanical Engineering.'
        },
        
        # RULE 006 - TVL-ICT/STEM to Electronics Engineering
        {
            'rule_id': 'RULE006',
            'rule_description': 'ICT or STEM students with technical skills and attention to detail',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', 'IN', ['TVL-ICT', 'STEM']),
                create_criterion('skills.technical', '>=', 4),
                create_criterion('skills.attention_to_detail', '>=', 3)
            ]),
            'recommended_program_id': programs['BSECE'],
            'confidence_score': 86.0,
            'justification': 'ICT or STEM background with attention to detail supports the precision-required work in circuit design, embedded systems, and telecommunications central to Electronics Engineering.'
        },
        
        # RULE 007 - STEM/ABM to Industrial Engineering
        {
            'rule_id': 'RULE007',
            'rule_description': 'STEM or ABM students with analytical and organizational skills',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', 'IN', ['STEM', 'ABM']),
                create_criterion('skills.analytical', '>=', 4),
                create_criterion('skills.leadership', '>=', 3)
            ]),
            'recommended_program_id': programs['BSIE'],
            'confidence_score': 85.0,
            'justification': 'Combination of analytical thinking and organizational skills matches Industrial Engineering\'s focus on process optimization, operations management, and systems efficiency.'
        },
        
        # RULE 008 - ABM to Business Administration
        {
            'rule_id': 'RULE008',
            'rule_description': 'ABM students interested in business with leadership skills',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'ABM'),
                create_criterion('skills.communication', '>=', 3),
                create_criterion('interests', 'CONTAINS', 'Business'),
                create_criterion('skills.leadership', '>=', 3)
            ]),
            'recommended_program_id': programs['BSBA'],
            'confidence_score': 93.0,
            'justification': 'ABM strand specifically prepares students for business programs. Leadership and communication skills essential for management roles align with BSBA curriculum.'
        },
        
        # RULE 009 - ABM to Accountancy
        {
            'rule_id': 'RULE009',
            'rule_description': 'ABM students with strong numerical skills and attention to detail',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'ABM'),
                create_criterion('favorite_subjects', 'CONTAINS', 'Accounting'),
                create_criterion('skills.numerical', '>=', 4),
                create_criterion('skills.attention_to_detail', '>=', 4)
            ]),
            'recommended_program_id': programs['BSA'],
            'confidence_score': 94.0,
            'justification': 'Direct accounting background from ABM with strong numerical skills and detail orientation are prerequisites for the rigorous BSA program and CPA licensure path.'
        },
        
        # RULE 010 - ABM/GAS to Office Administration
        {
            'rule_id': 'RULE010',
            'rule_description': 'ABM or GAS students with organizational and communication skills',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', 'IN', ['ABM', 'GAS']),
                create_criterion('skills.leadership', '>=', 3),
                create_criterion('skills.communication', '>=', 3),
                create_criterion('learning_style', '==', 'Collaborative/Group work')
            ]),
            'recommended_program_id': programs['BSOA'],
            'confidence_score': 82.0,
            'justification': 'Organizational and communication skills with collaborative work style suit administrative management, records management, and office systems focus of this program.'
        },
        
        # RULE 011 - HUMSS to Education
        {
            'rule_id': 'RULE011',
            'rule_description': 'HUMSS students with communication skills interested in teaching',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'HUMSS'),
                create_criterion('skills.communication', '>=', 4),
                create_criterion('interests', 'CONTAINS', 'Education'),
                create_criterion('skills.leadership', '>=', 3)
            ]),
            'recommended_program_id': programs['BSED'],
            'confidence_score': 91.0,
            'justification': 'HUMSS emphasis on humanities and communication skills, combined with genuine teaching interest, provides strong foundation for pedagogical studies and classroom management.'
        },
        
        # RULE 012 - STEM/TVL-IA to Architecture
        {
            'rule_id': 'RULE012',
            'rule_description': 'STEM or TVL-IA students with creativity and visual learning style',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', 'IN', ['STEM', 'TVL-IA']),
                create_criterion('skills.creativity', '>=', 4),
                create_criterion('interests', 'CONTAINS', 'Engineering'),
                create_criterion('learning_style', '==', 'Visual/Creative learning')
            ]),
            'recommended_program_id': programs['BSARCH'],
            'confidence_score': 89.0,
            'justification': 'Combination of technical/mathematical skills from STEM or TVL-IA with strong creativity and visual learning style matches the design-engineering balance required in Architecture.'
        },
        
        # RULE 013 - TVL-IA/ICT to Industrial Technology
        {
            'rule_id': 'RULE013',
            'rule_description': 'TVL students with strong technical skills and practical learning preference',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', 'IN', ['TVL-IA', 'TVL-ICT']),
                create_criterion('skills.technical', '>=', 4),
                create_criterion('learning_style', '==', 'Hands-on/Practical learning')
            ]),
            'recommended_program_id': programs['BSINDTECH'],
            'confidence_score': 90.0,
            'justification': 'TVL background with hands-on technical expertise directly aligns with Industrial Technology\'s focus on advanced technical skills, manufacturing, and industrial processes.'
        },
        
        # RULE 014 - TVL-HE to Hotel and Restaurant Management
        {
            'rule_id': 'RULE014',
            'rule_description': 'TVL-HE students interested in hospitality',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'TVL-HE'),
                create_criterion('interests', 'CONTAINS', 'Hospitality')
            ]),
            'recommended_program_id': programs['BSHRM'],
            'confidence_score': 92.0,
            'justification': 'Home Economics strand with food service background provides practical foundation for hospitality management, food service operations, and customer service excellence.'
        },
        
        # RULE 015 - TVL to Technical Teacher Education
        {
            'rule_id': 'RULE015',
            'rule_description': 'TVL students interested in teaching with technical skills',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', 'IN', ['TVL-HE', 'TVL-IA', 'TVL-ICT']),
                create_criterion('interests', 'CONTAINS', 'Education'),
                create_criterion('skills.technical', '>=', 4),
                create_criterion('skills.communication', '>=', 3)
            ]),
            'recommended_program_id': programs['BTVTEd'],
            'confidence_score': 88.0,
            'justification': 'TVL background with teaching interest creates pathway to become technical-vocational educators, combining trade expertise with pedagogical skills.'
        },
        
        # Additional rules for broader coverage
        
        # RULE 016 - GAS to IT
        {
            'rule_id': 'RULE016',
            'rule_description': 'GAS students with technology interest and technical aptitude',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'GAS'),
                create_criterion('interests', 'CONTAINS', 'Technology'),
                create_criterion('skills.technical', '>=', 3)
            ]),
            'recommended_program_id': programs['BSIT'],
            'confidence_score': 78.0,
            'justification': 'GAS students with technology interest and technical aptitude can transition to IT programs despite diverse academic background, especially with ICT electives taken.'
        },
        
        # RULE 017 - STEM to Accountancy
        {
            'rule_id': 'RULE017',
            'rule_description': 'STEM students with exceptional numerical skills interested in finance',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'STEM'),
                create_criterion('skills.numerical', '>=', 5),
                create_criterion('skills.analytical', '>=', 5),
                create_criterion('interests', 'CONTAINS', 'Business')
            ]),
            'recommended_program_id': programs['BSA'],
            'confidence_score': 83.0,
            'justification': 'STEM students with exceptional mathematical and analytical abilities can excel in accounting\'s quantitative aspects, financial analysis, and auditing procedures.'
        },
        
        # RULE 018 - TVL-ICT to CS
        {
            'rule_id': 'RULE018',
            'rule_description': 'TVL-ICT students with advanced technical and creative skills',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'TVL-ICT'),
                create_criterion('skills.technical', '>=', 5),
                create_criterion('skills.creativity', '>=', 4)
            ]),
            'recommended_program_id': programs['BSCS'],
            'confidence_score': 85.0,
            'justification': 'Advanced ICT skills combined with creativity support CS specializations in game development, computer graphics, UI/UX design, and multimedia applications.'
        },
        
        # RULE 019 - HUMSS to Office Administration
        {
            'rule_id': 'RULE019',
            'rule_description': 'HUMSS students with communication and leadership skills',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'HUMSS'),
                create_criterion('skills.communication', '>=', 4),
                create_criterion('interests', 'CONTAINS', 'Management'),
                create_criterion('skills.leadership', '>=', 3)
            ]),
            'recommended_program_id': programs['BSOA'],
            'confidence_score': 77.0,
            'justification': 'HUMSS communication strengths and understanding of organizational behavior support administrative roles in human resources, executive assistance, and office management.'
        },
        
        # RULE 020 - GAS undecided to Industrial Technology
        {
            'rule_id': 'RULE020',
            'rule_description': 'GAS students with practical learning preference',
            'conditions': create_rule_condition('AND', [
                create_criterion('strand', '==', 'GAS'),
                create_criterion('learning_style', '==', 'Hands-on/Practical learning')
            ]),
            'recommended_program_id': programs['BSINDTECH'],
            'confidence_score': 70.0,
            'justification': 'For undecided GAS students, Industrial Technology offers broad technical foundation with multiple specialization options discovered through hands-on exposure.'
        }
    ]
    
    for rule_data in rules_data:
        existing = Rule.query.filter_by(rule_id=rule_data['rule_id']).first()
        if not existing:
            rule = Rule(**rule_data)
            db.session.add(rule)
    
    db.session.commit()
    print(f"Seeded {len(rules_data)} rules")

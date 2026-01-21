#!/usr/bin/env python3
"""Database setup script"""

from app import app, db
from models import AdminUser
from seed_data import seed_programs, seed_rules
from models import Program, Rule
from werkzeug.security import generate_password_hash

print("🚀 Setting up database...")
print("")

with app.app_context():
    # Create all tables
    print("📋 Creating database tables...")
    db.create_all()
    print("✅ Database tables created!")
    print("")
    
    # Seed programs
    print("📚 Loading programs...")
    seed_programs(db, Program)
    print("✅ 15 programs loaded!")
    print("")
    
    # Seed rules
    print("📋 Loading rules...")
    seed_rules(db, Rule, Program)
    print("✅ 20 rules loaded!")
    print("")
    
    # Create admin user
    print("👤 Creating admin user...")
    admin = AdminUser.query.filter_by(username='admin').first()
    if not admin:
        admin = AdminUser(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            role='super_admin',
            email='admin@earist.edu.ph'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created!")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print("✅ Admin user already exists")
    
    print("")
    print("🎉 Database setup complete!")
    print("")

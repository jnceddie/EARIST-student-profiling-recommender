#!/bin/bash

clear
echo "========================================"
echo "  STARTING ERVHS-EARIST SYSTEM"
echo "========================================"
echo ""

source venv/bin/activate
cd backend

echo "✅ System starting..."
echo ""
echo "🌐 Access URLs:"
echo "   Student: http://localhost:5000"
echo "   Admin:   http://localhost:5000/admin/login"
echo ""
echo "🔐 Admin Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "Press Ctrl+C to stop"
echo "========================================"
echo ""

python3 app.py

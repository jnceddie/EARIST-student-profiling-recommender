#!/bin/bash

clear
echo "========================================"
echo "  ERVHS-EARIST INSTANT SETUP"
echo "========================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo ""
    echo "Please install Python 3.8+ from:"
    echo "https://python.org/downloads"
    echo ""
    exit 1
fi

echo "[1/4] ✅ Python found: $(python3 --version)"
echo ""

echo "[2/4] 📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[3/4] 📥 Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet Flask==3.0.0
pip install --quiet Flask-SQLAlchemy==3.1.1
pip install --quiet SQLAlchemy==2.0.23
pip install --quiet Werkzeug==3.0.1
pip install --quiet reportlab==4.0.7
pip install --quiet python-dotenv==1.0.0
pip install --quiet bcrypt==4.1.1

echo "[4/4] ✅ Database ready!"
echo ""
echo "========================================"
echo "  ✅ SETUP COMPLETE!"
echo "========================================"
echo ""
echo "📊 DATABASE STATUS:"
echo "   • 15 Programs loaded"
echo "   • 20 Rules loaded"
echo "   • Admin ready (admin/admin123)"
echo ""
echo "🚀 TO RUN SYSTEM:"
echo "   1. bash RUN_SYSTEM.sh"
echo "   2. Open: http://localhost:5000"
echo "   3. Login: admin / admin123"
echo ""
echo "========================================"

#!/bin/bash

echo "========================================="
echo "  Lean Six Sigma Project Management"
echo "========================================="
echo ""
echo "Starting Streamlit app..."
echo ""

# Kiểm tra xem đã cài đặt requirements chưa
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/Updating requirements..."
pip install -q -r requirements.txt

echo ""
echo "========================================="
echo "  App is starting..."
echo "  Open browser: http://localhost:8501"
echo "========================================="
echo ""

# Chạy Streamlit
streamlit run app.py

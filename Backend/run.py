#!/usr/bin/env python3
"""
Simple script to run the Student Attendance System
"""

import os
import sys

def main():
    print("=" * 50)
    print("Student Attendance Registration System")
    print("=" * 50)
    print("Starting the application...")
    print("Access the application at: http://localhost:5000")
    print("Default Admin Login:")
    print("  Email: admin@school.com")
    print("  Password: admin123")
    print("=" * 50)
    
    # Import and run the Flask app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Script to help save the uploaded images to the static folder
Run this script and follow the instructions to save your images
"""

import os
import shutil
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    static_dir = Path("static")
    images_dir = static_dir / "images"
    
    static_dir.mkdir(exist_ok=True)
    images_dir.mkdir(exist_ok=True)
    
    print("✅ Created directories: static/images/")
    return images_dir

def save_images():
    """Instructions for saving images"""
    images_dir = create_directories()
    
    print("\n" + "="*60)
    print("📸 IMAGE SAVING INSTRUCTIONS")
    print("="*60)
    
    print("\n1️⃣ BACKGROUND IMAGE (College Building):")
    print(f"   Save as: {images_dir}/college-background.jpg")
    print("   This will be used as the full-screen background")
    
    print("\n2️⃣ LOGO IMAGE (NIELIT Logo):")
    print(f"   Save as: {images_dir}/nielit-logo.png")
    print("   This will be used as the website logo (transparent background)")
    
    print("\n3️⃣ After saving the images, update the CSS:")
    print("   The background image will be automatically applied")
    print("   The logo will appear in the navigation bar")
    
    print("\n🎨 CURRENT FEATURES:")
    print("   ✅ Glassmorphism login card")
    print("   ✅ Modern navigation bar")
    print("   ✅ Animated particles")
    print("   ✅ Responsive design")
    print("   ✅ Demo credentials")
    print("   ✅ Form validation")
    print("   ✅ Loading animations")
    
    print("\n🌐 ACCESS YOUR APPLICATION:")
    print("   URL: http://localhost:5000")
    print("   Admin: admin@school.com / admin123")
    
    print("\n" + "="*60)
    print("Your modern glassmorphism login page is ready! 🎉")
    print("="*60)

if __name__ == "__main__":
    save_images()
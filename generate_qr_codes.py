#!/usr/bin/env python
"""
Script to generate QR codes for existing students
Run this script to ensure all students have QR codes
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quitescan.settings')
django.setup()

from attendance.models import Student

def generate_missing_qr_codes():
    """Generate QR codes for students who don't have them"""
    students_without_qr = Student.objects.filter(qr_image='')
    students_with_empty_qr_code = Student.objects.filter(qr_code='')
    
    print(f"Found {students_without_qr.count()} students without QR images")
    print(f"Found {students_with_empty_qr_code.count()} students without QR codes")
    
    # Generate QR codes for students without QR code strings
    for student in students_with_empty_qr_code:
        print(f"Generating QR code for {student.first_name} {student.last_name} ({student.student_id})")
        student.save()  # This will trigger QR code generation
    
    # Generate QR images for students without images
    for student in students_without_qr:
        if student.qr_code:  # Only if they have a QR code string
            print(f"Generating QR image for {student.first_name} {student.last_name} ({student.student_id})")
            student.generate_qr_code()
    
    print("QR code generation completed!")

if __name__ == '__main__':
    generate_missing_qr_codes()
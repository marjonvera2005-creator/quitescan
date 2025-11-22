from django.core.management.base import BaseCommand
from attendance.models import Student

class Command(BaseCommand):
    help = 'Test QR code generation for a specific student'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=str, help='Student ID to test QR generation')

    def handle(self, *args, **options):
        student_id = options['student_id']
        
        try:
            student = Student.objects.get(student_id=student_id)
            self.stdout.write(f"Found student: {student.first_name} {student.last_name}")
            self.stdout.write(f"Current QR code: {student.qr_code}")
            self.stdout.write(f"QR image exists: {bool(student.qr_image)}")
            
            if student.qr_image:
                self.stdout.write(f"QR image path: {student.qr_image.url}")
            else:
                self.stdout.write("Generating QR code...")
                student.generate_qr_code()
                self.stdout.write(f"QR code generated: {student.qr_image.url if student.qr_image else 'Failed'}")
                
        except Student.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Student with ID '{student_id}' not found"))
            
            # List available students
            students = Student.objects.all()[:5]
            if students:
                self.stdout.write("Available students:")
                for s in students:
                    self.stdout.write(f"  - {s.student_id}: {s.first_name} {s.last_name}")
            else:
                self.stdout.write("No students found in database")
from django.core.management.base import BaseCommand
from attendance.models import Student

class Command(BaseCommand):
    help = 'Generate QR codes for students who do not have them'

    def handle(self, *args, **options):
        students_without_qr = Student.objects.filter(qr_image='')
        students_with_empty_qr_code = Student.objects.filter(qr_code='')
        
        self.stdout.write(f"Found {students_without_qr.count()} students without QR images")
        self.stdout.write(f"Found {students_with_empty_qr_code.count()} students without QR codes")
        
        # Generate QR codes for students without QR code strings
        for student in students_with_empty_qr_code:
            self.stdout.write(f"Generating QR code for {student.first_name} {student.last_name} ({student.student_id})")
            student.save()  # This will trigger QR code generation
        
        # Generate QR images for students without images
        for student in students_without_qr:
            if student.qr_code:  # Only if they have a QR code string
                self.stdout.write(f"Generating QR image for {student.first_name} {student.last_name} ({student.student_id})")
                student.generate_qr_code()
        
        self.stdout.write(self.style.SUCCESS("QR code generation completed!"))
from django.core.management.base import BaseCommand
from attendance.models import Student, Department
import uuid

class Command(BaseCommand):
    help = 'Test student registration and QR code generation'

    def handle(self, *args, **options):
        # Get or create a test department
        department, created = Department.objects.get_or_create(
            code='TEST',
            defaults={
                'name': 'Test Department',
                'description': 'Test department for QR code generation',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(f"Created test department: {department}")
        else:
            self.stdout.write(f"Using existing department: {department}")
        
        # Create a test student
        test_id = f"TEST-{uuid.uuid4().hex[:8].upper()}"
        
        try:
            student = Student.objects.create(
                student_id=test_id,
                first_name='Test',
                last_name='Student',
                email=f'test.{test_id.lower()}@example.com',
                department=department,
                registration_status='approved'
            )
            
            self.stdout.write(f"Created student: {student}")
            self.stdout.write(f"QR Code: {student.qr_code}")
            self.stdout.write(f"QR Image exists: {bool(student.qr_image)}")
            
            if student.qr_image:
                self.stdout.write(f"QR Image path: {student.qr_image.url}")
                self.stdout.write(self.style.SUCCESS("✅ QR code generation successful!"))
            else:
                self.stdout.write(self.style.ERROR("❌ QR code generation failed!"))
                
            # Clean up - delete the test student
            student.delete()
            self.stdout.write("Test student deleted")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating student: {e}"))
from django.db import models
from django.contrib.auth.models import User
import uuid

try:
    import qrcode
    from io import BytesIO
    from django.core.files import File
    from PIL import Image
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Student(models.Model):
    REGISTRATION_STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    qr_code = models.CharField(max_length=255, unique=True, blank=True)
    qr_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    registration_status = models.CharField(max_length=10, choices=REGISTRATION_STATUS_CHOICES, default='pending')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_students')
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate QR code string if not exists
        if not self.qr_code:
            self.qr_code = str(uuid.uuid4())
        
        # Save the model first
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Generate QR image after saving
        if QR_AVAILABLE and (is_new or not self.qr_image):
            try:
                self.generate_qr_code()
            except Exception as e:
                print(f"QR generation error: {e}")

    def generate_qr_code(self):
        if not QR_AVAILABLE or not self.qr_code:
            return
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.qr_code)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        filename = f'qr_code_{self.student_id}.png'
        self.qr_image.save(filename, File(buffer), save=False)
        Student.objects.filter(pk=self.pk).update(qr_image=self.qr_image)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class AttendanceLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    action = models.CharField(max_length=3, choices=[('IN', 'Check In'), ('OUT', 'Check Out')])
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.action} at {self.timestamp}"

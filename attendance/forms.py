from django import forms
from .models import Student, Department

class StudentSelfRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'department', 'phone_number', 'address', 'date_of_birth']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Student ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter Email Address'}),
            'department': forms.Select(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Enter Address', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.filter(is_active=True)
        self.fields['department'].empty_label = "Select a Department"

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'department', 'phone_number', 'address', 'date_of_birth']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Student ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter Email Address'}),
            'department': forms.Select(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Enter Address', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.filter(is_active=True)
        self.fields['department'].empty_label = "Select a Department"

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Department Name'}),
            'code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Department Code'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Enter Department Description', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

class StudentApprovalForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['registration_status', 'rejection_reason']
        widgets = {
            'registration_status': forms.Select(attrs={'class': 'form-input'}),
            'rejection_reason': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Enter rejection reason (if rejecting)', 'rows': 3}),
        }

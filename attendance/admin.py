from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Student, AttendanceLog, Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'department', 'registration_status', 'status', 'qr_code_display', 'created_at']
    list_filter = ['registration_status', 'status', 'department', 'created_at']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    readonly_fields = ['qr_code', 'qr_image_display', 'approved_by', 'approved_at']
    fieldsets = (
        ('Student Information', {
            'fields': ('student_id', 'first_name', 'last_name', 'email', 'department', 'phone_number', 'address', 'date_of_birth')
        }),
        ('Registration Status', {
            'fields': ('registration_status', 'approved_by', 'approved_at', 'rejection_reason')
        }),
        ('Account Status', {
            'fields': ('status',)
        }),
        ('QR Code Information', {
            'fields': ('qr_code', 'qr_image_display'),
            'classes': ('collapse',)
        }),
    )
    change_form_template = 'admin/attendance/student/change_form.html'
    change_list_template = 'admin/attendance/student/change_list.html'
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['qr_codes_url'] = '/qr-codes/'
        return super().changelist_view(request, extra_context)
    
    actions = ['view_qr_codes']
    
    def view_qr_codes(self, request, queryset):
        from django.shortcuts import redirect
        return redirect('qr_codes')
    view_qr_codes.short_description = "View QR Codes for selected students"

    def qr_code_display(self, obj):
        if obj.qr_code:
            return format_html('<span style="font-family: monospace; font-size: 10px;">{}</span>', obj.qr_code[:20] + '...')
        return 'No QR Code'
    qr_code_display.short_description = 'QR Code'

    def qr_image_display(self, obj):
        if obj.qr_image:
            return format_html(
                '<div style="text-align: center;">'
                '<img src="{}" style="max-width: 200px; height: auto; border: 2px solid #ddd; border-radius: 8px;" />'
                '<br><br>'
                '<strong>QR Code Text:</strong><br>'
                '<span style="font-family: monospace; background: #f5f5f5; padding: 5px; border-radius: 3px;">{}</span>'
                '<br><br>'
                '<a href="{}" class="button" target="_blank">Download QR Code</a>'
                '</div>',
                obj.qr_image.url,
                obj.qr_code,
                obj.qr_image.url
            )
        return 'QR Code not generated yet'
    qr_image_display.short_description = 'QR Code Image'

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'action', 'department', 'timestamp']
    list_filter = ['action', 'department', 'timestamp']
    search_fields = ['student__first_name', 'student__last_name', 'student__student_id']
    readonly_fields = ['timestamp']

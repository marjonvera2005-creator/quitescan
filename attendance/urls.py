from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-gate/', views.admin_gate, name='admin_gate'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register-student/', views.register_student, name='register_student'),
    path('students/', views.student_list, name='student_list'),
    path('report/', views.attendance_report, name='attendance_report'),
    path('report/monthly-all/', views.monthly_attendance_all, name='monthly_attendance_all'),
    path('report/weekly-all/', views.weekly_attendance_all, name='weekly_attendance_all'),
    path('qr-codes/', views.qr_codes_view, name='qr_codes'),
    path('student/scan/', views.student_scan, name='student_scan'),
    path('student/process-scan/', views.process_scan, name='process_scan'),
    path('student/register/', views.student_register, name='student_register'),
    path('student/registration-success/', views.registration_success, name='registration_success'),
    path('admin/pending-registrations/', views.pending_registrations, name='pending_registrations'),
    path('admin/approve-student/<int:student_id>/', views.approve_student, name='approve_student'),
    path('admin/manage-departments/', views.manage_departments, name='manage_departments'),
    path('admin/edit-department/<int:department_id>/', views.edit_department, name='edit_department'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('sw.js', views.service_worker, name='service_worker'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
]

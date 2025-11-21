from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth, TruncWeek, TruncYear
from datetime import datetime, timedelta
from collections import defaultdict
import os
from .models import Student, AttendanceLog, Department
from .forms import StudentRegistrationForm, StudentSelfRegistrationForm, DepartmentForm, StudentApprovalForm
import json

def index(request):
    """Landing page for QUITESCAN"""
    return render(request, 'attendance/index.html')

def student_register(request):
    """Student self-registration page"""
    if request.method == 'POST':
        form = StudentSelfRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.registration_status = 'pending'
            student.save()
            messages.success(request, 'Registration submitted successfully! Please wait for admin approval.')
            return redirect('registration_success')
    else:
        form = StudentSelfRegistrationForm()
    
    return render(request, 'attendance/student/register.html', {'form': form})

def registration_success(request):
    """Registration success page"""
    return render(request, 'attendance/student/registration_success.html')


def admin_gate(request):
    """Pre-password gate before accessing Django admin/login"""
    ADMIN_GATE_PASSWORD = os.environ.get('ADMIN_GATE_PASSWORD', 'admin123')
    if request.method == 'POST':
        password = request.POST.get('password', '')
        if password == ADMIN_GATE_PASSWORD:
            # Set a simple session flag
            request.session['admin_gate_ok'] = True
            # Redirect to admin dashboard
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Incorrect password')
    
    return render(request, 'attendance/admin/gate.html')

@staff_member_required
def admin_dashboard(request):
    """Admin dashboard to view attendance logs"""
    # Year selection for yearly stats
    current_year = timezone.now().year
    selected_year_param = request.GET.get('year')
    try:
        selected_year = int(selected_year_param) if selected_year_param else current_year
    except ValueError:
        selected_year = current_year
    year_options = [current_year + i for i in range(0, 6)]

    # Activity search inputs
    activity_search_query = request.GET.get('activity_search', '').strip()
    activity_month_str = request.GET.get('activity_month', timezone.now().strftime('%Y-%m'))
    activity_month_display = None
    activity_login_count = None
    activity_month_year = None
    activity_month_month = None
    try:
        activity_month_dt = datetime.strptime(activity_month_str, '%Y-%m')
        activity_month_display = activity_month_dt.strftime('%B %Y')
        activity_month_year = activity_month_dt.year
        activity_month_month = activity_month_dt.month
    except ValueError:
        activity_month_str = timezone.now().strftime('%Y-%m')
        activity_month_dt = datetime.strptime(activity_month_str, '%Y-%m')
        activity_month_display = activity_month_dt.strftime('%B %Y')
        activity_month_year = activity_month_dt.year
        activity_month_month = activity_month_dt.month

    # Get today's attendance
    today = timezone.now().date()
    today_logs = AttendanceLog.objects.filter(timestamp__date=today)
    
    # Get currently checked in students with pagination
    checked_in_students_list = []
    for student in Student.objects.filter(status='active'):
        last_log = AttendanceLog.objects.filter(student=student).first()
        if last_log and last_log.action == 'IN':
            checked_in_students_list.append(student)
    
    paginator_checked_in = Paginator(checked_in_students_list, 10)
    page_checked_in = request.GET.get('page_checked_in', 1)
    try:
        checked_in_students = paginator_checked_in.page(page_checked_in)
    except PageNotAnInteger:
        checked_in_students = paginator_checked_in.page(1)
    except EmptyPage:
        checked_in_students = paginator_checked_in.page(paginator_checked_in.num_pages)
    
    # Get recent attendance logs with pagination and filtering
    recent_logs_queryset = AttendanceLog.objects.select_related('student', 'department').order_by('-timestamp')
    
    # Apply month filter first
    if activity_month_year and activity_month_month:
        recent_logs_queryset = recent_logs_queryset.filter(
            timestamp__year=activity_month_year,
            timestamp__month=activity_month_month
        )
    
    # Apply search filter
    if activity_search_query:
        recent_logs_queryset = recent_logs_queryset.filter(
            Q(student__first_name__icontains=activity_search_query) |
            Q(student__last_name__icontains=activity_search_query) |
            Q(student__student_id__icontains=activity_search_query)
        )

    paginator_logs = Paginator(recent_logs_queryset, 10)
    page_logs = request.GET.get('page_logs', 1)
    try:
        recent_logs = paginator_logs.page(page_logs)
    except PageNotAnInteger:
        recent_logs = paginator_logs.page(1)
    except EmptyPage:
        recent_logs = paginator_logs.page(paginator_logs.num_pages)
    
    # Get department check-in statistics (unique students per department)
    department_stats = AttendanceLog.objects.filter(
        action='IN',
        timestamp__date=today
    ).values(
        'department__name',
        'department__code'
    ).annotate(
        check_in_count=Count('student', distinct=True)
    ).order_by('-check_in_count')
    
    # Get yearly check-in statistics for selected year
    yearly_check_ins = AttendanceLog.objects.filter(
        action='IN',
        timestamp__year=selected_year
    ).aggregate(
        total_unique_students=Count('student', distinct=True)
    )

    # Activity search calculation - count check-ins for searched student
    activity_login_count = None
    if activity_search_query:
        activity_logs = AttendanceLog.objects.filter(
            action='IN'
        )
        # Filter by student search
        activity_logs = activity_logs.filter(
            Q(student__first_name__icontains=activity_search_query) |
            Q(student__last_name__icontains=activity_search_query) |
            Q(student__student_id__icontains=activity_search_query)
        )
        # Filter by month if provided
        if activity_month_year and activity_month_month:
            activity_logs = activity_logs.filter(
                timestamp__year=activity_month_year,
                timestamp__month=activity_month_month
            )
        activity_login_count = activity_logs.count()
    
    context = {
        'today_logs': today_logs,
        'checked_in_students': checked_in_students,
        'recent_logs': recent_logs,
        'total_students': Student.objects.filter(status='active').count(),
        'today_count': today_logs.count(),
        'department_stats': department_stats,
        'yearly_check_ins': yearly_check_ins['total_unique_students'] or 0,
        'current_year': current_year,
        'selected_year': selected_year,
        'year_options': year_options,
        'activity_search_query': activity_search_query,
        'activity_month_str': activity_month_str,
        'activity_month_display': activity_month_display,
        'activity_login_count': activity_login_count if activity_search_query else None,
    }
    return render(request, 'attendance/admin/dashboard.html', context)

@staff_member_required
def register_student(request):
    """Register a new student and generate QR code"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.registration_status = 'approved'
            student.approved_by = request.user
            student.approved_at = timezone.now()
            student.save()
            messages.success(request, f'Student {student.first_name} {student.last_name} registered successfully!')
            return redirect('admin_dashboard')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'attendance/admin/register_student.html', {'form': form})

@staff_member_required
def pending_registrations(request):
    """View and manage pending student registrations"""
    pending_students = Student.objects.filter(registration_status='pending').order_by('-created_at')
    return render(request, 'attendance/admin/pending_registrations.html', {'students': pending_students})

@staff_member_required
def approve_student(request, student_id):
    """Approve or reject a student registration"""
    student = get_object_or_404(Student, id=student_id, registration_status='pending')
    
    if request.method == 'POST':
        form = StudentApprovalForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            if student.registration_status == 'approved':
                student.approved_by = request.user
                student.approved_at = timezone.now()
                student.rejection_reason = None
            elif student.registration_status == 'rejected':
                student.approved_by = None
                student.approved_at = None
            student.save()
            
            status_text = 'approved' if student.registration_status == 'approved' else 'rejected'
            messages.success(request, f'Student registration {status_text} successfully!')
            return redirect('pending_registrations')
    else:
        form = StudentApprovalForm(instance=student)
    
    return render(request, 'attendance/admin/approve_student.html', {'form': form, 'student': student})

@staff_member_required
def manage_departments(request):
    """Manage departments"""
    departments = Department.objects.all().order_by('name')
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully!')
            return redirect('manage_departments')
    else:
        form = DepartmentForm()
    
    return render(request, 'attendance/admin/manage_departments.html', {'departments': departments, 'form': form})

@staff_member_required
def edit_department(request, department_id):
    """Edit a department"""
    department = get_object_or_404(Department, id=department_id)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('manage_departments')
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'attendance/admin/edit_department.html', {'form': form, 'department': department})

def student_scan(request):
    """QR scanning page for students"""
    return render(request, 'attendance/student/scan.html')

@csrf_exempt
def process_scan(request):
    """Process QR code scan and log attendance"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_code = data.get('qr_code')
            
            if not qr_code:
                return JsonResponse({'success': False, 'message': 'QR code is required'})
            
            # Find student by QR code
            student = get_object_or_404(Student, qr_code=qr_code, status='active')
            
            # Check if student is currently checked in
            last_log = AttendanceLog.objects.filter(student=student).first()
            
            if last_log and last_log.action == 'IN':
                # Student is checked in, check them out
                action = 'OUT'
                message = f'Checked out successfully, {student.first_name}!'
            else:
                # Student is not checked in, check them in
                action = 'IN'
                message = f'Checked in successfully, {student.first_name}!'
            
            # Create attendance log with department information
            AttendanceLog.objects.create(student=student, action=action, department=student.department)
            
            return JsonResponse({
                'success': True,
                'message': message,
                'student_name': f'{student.first_name} {student.last_name}',
                'action': action,
                'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid QR code'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@staff_member_required
def student_list(request):
    """View all registered students"""
    students_list = Student.objects.all().order_by('first_name')
    paginator = Paginator(students_list, 10)
    page = request.GET.get('page', 1)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    return render(request, 'attendance/admin/student_list.html', {'students': students})

@staff_member_required
def attendance_report(request):
    """Generate attendance report"""
    # Get date range (default to today)
    date_str = request.GET.get('date', timezone.now().strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = timezone.now().date()
    
    # Get attendance logs for selected date
    logs = AttendanceLog.objects.filter(timestamp__date=selected_date)
    
    # Group by student
    student_attendance = {}
    for log in logs:
        if log.student not in student_attendance:
            student_attendance[log.student] = {'check_in': None, 'check_out': None}
        
        if log.action == 'IN':
            student_attendance[log.student]['check_in'] = log.timestamp
        elif log.action == 'OUT':
            student_attendance[log.student]['check_out'] = log.timestamp
    
    # Calculate present students before pagination
    present_students_count = len([s for s in student_attendance.keys() if student_attendance[s]['check_in']])
    
    # Convert to list for pagination
    student_attendance_list = list(student_attendance.items())
    paginator = Paginator(student_attendance_list, 10)
    page = request.GET.get('page', 1)
    try:
        student_attendance_page = paginator.page(page)
    except PageNotAnInteger:
        student_attendance_page = paginator.page(1)
    except EmptyPage:
        student_attendance_page = paginator.page(paginator.num_pages)
    
    # Calculate monthly attendance summary - get latest month only
    latest_monthly = AttendanceLog.objects.filter(
        action='IN'
    ).annotate(
        month=TruncMonth('timestamp')
    ).values('month').annotate(
        unique_students=Count('student', distinct=True)
    ).order_by('-month').first()
    
    monthly_summary = None
    if latest_monthly:
        monthly_summary = {
            'month': latest_monthly['month'],
            'count': latest_monthly['unique_students']
        }
    
    # Calculate weekly attendance summary - get latest week only
    latest_weekly = AttendanceLog.objects.filter(
        action='IN'
    ).annotate(
        week=TruncWeek('timestamp')
    ).values('week').annotate(
        unique_students=Count('student', distinct=True)
    ).order_by('-week').first()
    
    weekly_summary = None
    weekly_summary_start = None
    weekly_summary_end = None
    if latest_weekly:
        weekly_summary = {
            'week': latest_weekly['week'],
            'count': latest_weekly['unique_students']
        }
        weekly_summary_start = latest_weekly['week']
        weekly_summary_end = latest_weekly['week'] + timedelta(days=6)
    
    # Get department check-in statistics for selected date (unique students per department)
    department_stats = AttendanceLog.objects.filter(
        action='IN',
        timestamp__date=selected_date
    ).values(
        'department__name',
        'department__code'
    ).annotate(
        check_in_count=Count('student', distinct=True)
    ).order_by('-check_in_count')
    
    context = {
        'selected_date': selected_date,
        'student_attendance': dict(student_attendance_page.object_list),
        'student_attendance_page': student_attendance_page,
        'total_students': Student.objects.filter(status='active').count(),
        'present_students': present_students_count,
        'monthly_summary': monthly_summary,
        'weekly_summary': weekly_summary,
        'weekly_summary_start': weekly_summary_start,
        'weekly_summary_end': weekly_summary_end,
        'department_stats': department_stats,
    }
    return render(request, 'attendance/admin/attendance_report.html', context)

@staff_member_required
def monthly_attendance_all(request):
    """View all monthly attendance records"""
    departments = Department.objects.all().order_by('name')
    selected_department_id = request.GET.get('department', '')
    selected_month_str = request.GET.get('month', timezone.now().strftime('%Y-%m'))
    selected_month_display = None
    selected_month_total = None
    selected_department = None

    monthly_queryset = AttendanceLog.objects.filter(action='IN')
    if selected_department_id:
        monthly_queryset = monthly_queryset.filter(department_id=selected_department_id)
        selected_department = Department.objects.filter(id=selected_department_id).first()

    try:
        selected_month_dt = datetime.strptime(selected_month_str, '%Y-%m')
        selected_month_display = selected_month_dt.strftime('%B %Y')
        selected_month_total = monthly_queryset.filter(
            timestamp__year=selected_month_dt.year,
            timestamp__month=selected_month_dt.month
        ).aggregate(total=Count('student', distinct=True))['total'] or 0
    except ValueError:
        selected_month_str = timezone.now().strftime('%Y-%m')
        selected_month_total = None
        selected_month_display = None

    monthly_data = monthly_queryset.annotate(
        month=TruncMonth('timestamp')
    ).values('month').annotate(
        unique_students=Count('student', distinct=True)
    ).order_by('-month')
    
    paginator = Paginator(monthly_data, 10)
    page = request.GET.get('page', 1)
    try:
        monthly_page = paginator.page(page)
    except PageNotAnInteger:
        monthly_page = paginator.page(1)
    except EmptyPage:
        monthly_page = paginator.page(paginator.num_pages)
    
    return render(request, 'attendance/admin/monthly_attendance_all.html', {
        'monthly_page': monthly_page,
        'departments': departments,
        'selected_department_id': str(selected_department_id),
        'selected_department': selected_department,
        'selected_month_str': selected_month_str,
        'selected_month_display': selected_month_display,
        'selected_month_total': selected_month_total,
    })

@staff_member_required
def weekly_attendance_all(request):
    """View all weekly attendance records"""
    month_param = request.GET.get('month', '').strip()
    selected_month_display = None
    selected_month_year = None
    selected_month_month = None
    if month_param:
        try:
            month_dt = datetime.strptime(month_param, '%Y-%m')
            selected_month_display = month_dt.strftime('%B %Y')
            selected_month_year = month_dt.year
            selected_month_month = month_dt.month
        except ValueError:
            month_param = ''

    month_options_qs = AttendanceLog.objects.filter(
        action='IN'
    ).annotate(
        month=TruncMonth('timestamp')
    ).values_list('month', flat=True).distinct().order_by('-month')
    month_options = [
        {'value': month.strftime('%Y-%m'), 'label': month.strftime('%B %Y')}
        for month in month_options_qs if month
    ]

    weekly_queryset = AttendanceLog.objects.filter(action='IN')
    if selected_month_year and selected_month_month:
        weekly_queryset = weekly_queryset.filter(
            timestamp__year=selected_month_year,
            timestamp__month=selected_month_month
        )

    weekly_data_queryset = weekly_queryset.annotate(
        week=TruncWeek('timestamp')
    ).values('week').annotate(
        unique_students=Count('student', distinct=True)
    ).order_by('-week')

    weekly_data = []
    for entry in weekly_data_queryset:
        entry = dict(entry)
        entry['week_end'] = entry['week'] + timedelta(days=6)
        weekly_data.append(entry)
    
    paginator = Paginator(weekly_data, 10)
    page = request.GET.get('page', 1)
    try:
        weekly_page = paginator.page(page)
    except PageNotAnInteger:
        weekly_page = paginator.page(1)
    except EmptyPage:
        weekly_page = paginator.page(paginator.num_pages)
    
    return render(request, 'attendance/admin/weekly_attendance_all.html', {
        'weekly_page': weekly_page,
        'month_options': month_options,
        'selected_month_str': month_param,
        'selected_month_display': selected_month_display,
    })

@staff_member_required
def qr_codes_view(request):
    """Display all student QR codes"""
    students_list = Student.objects.filter(status='active').order_by('first_name')
    paginator = Paginator(students_list, 10)
    page = request.GET.get('page', 1)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    return render(request, 'attendance/admin/qr_codes.html', {'students': students})


@staff_member_required
def admin_logout(request):
    """Custom logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

def service_worker(request):
    """Service Worker for offline caching"""
    sw_js = """
    const CACHE_NAME = 'quitescan-cache-v1';
    const PRECACHE_URLS = [
      '/',
      '/student/scan/',
      '/admin/login/',
      '/static/js/tw.js',
      '/static/js/jsQR.min.js',
      '/static/css/custom.css',
      '/static/images/Quitescan logo.png',
    ];

    self.addEventListener('install', event => {
      event.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_URLS)).then(self.skipWaiting())
      );
    });

    self.addEventListener('activate', event => {
      event.waitUntil(
        caches.keys().then(keys => Promise.all(keys.map(k => { if (k !== CACHE_NAME) { return caches.delete(k); } }))).then(self.clients.claim())
      );
    });

    self.addEventListener('fetch', event => {
      if (event.request.method !== 'GET') return;
      event.respondWith(
        caches.match(event.request).then(cached => {
          const fetchPromise = fetch(event.request).then(response => {
            const copy = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy)).catch(()=>{});
            return response;
          }).catch(() => cached);
          return cached || fetchPromise;
        })
      );
    });
    """
    return HttpResponse(sw_js, content_type='application/javascript')

# QUITESCAN - Student Attendance System

A modern, Django-based attendance system designed for students studying, resting, or meeting. Features QR code scanning for seamless check-in/out processes with a beautiful yellow-themed UI.

## 🌟 Features

- **QR Code Generation**: Automatic QR code generation for each student
- **Real-time Scanning**: Camera-based QR code scanning with fallback manual entry
- **Admin Dashboard**: Comprehensive overview of attendance statistics
- **Student Management**: Register, view, and manage student information
- **Attendance Reports**: Detailed reports with export functionality
- **Beautiful UI**: Modern design with Tailwind CSS and yellow theme
- **Responsive Design**: Works perfectly on desktop and mobile devices

## 🏗️ Project Structure

```
quitescan/
├── quitescan/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Project configuration
│   ├── urls.py               # Main URL routing
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
├── attendance/               # Main app
│   ├── __init__.py
│   ├── admin.py              # Django admin configuration
│   ├── apps.py               # App configuration
│   ├── forms.py              # Student registration form
│   ├── models.py             # Database models
│   ├── urls.py               # App URL routing
│   └── views.py              # View functions
├── templates/                # HTML templates
│   ├── base.html             # Base template
│   └── attendance/           # App-specific templates
│       ├── index.html        # Landing page
│       ├── admin/            # Admin templates
│       └── student/          # Student templates
├── static/                   # Static files
│   └── css/                  # Custom CSS
├── media/                    # Uploaded files (QR codes)
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8+
- MySQL 5.7+
- pip

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd quitescan
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   # Create MySQL database
   mysql -u root -p
   CREATE DATABASE quitescan_db;
   EXIT;
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 📱 Usage

### For Students

1. **Access the scanning page**: Navigate to `/student/scan/`
2. **Scan QR Code**: Use your phone's camera to scan the QR code
3. **Manual Entry**: If camera access is denied, manually enter the QR code
4. **Check In/Out**: The system automatically determines if you're checking in or out

### For Administrators

1. **Login**: Access `/admin/` with your superuser credentials
2. **Dashboard**: View real-time attendance statistics at `/admin/dashboard/`
3. **Register Students**: Add new students at `/admin/register-student/`
4. **View Reports**: Generate attendance reports at `/admin/report/`
5. **Manage Students**: View all students at `/admin/students/`

## 🎨 Design Features

- **Yellow Theme**: Perfect for student environments (studying, resting, meeting)
- **Gradient Backgrounds**: Beautiful yellow-to-orange gradients
- **Responsive Cards**: Modern card-based layout
- **Hover Effects**: Interactive elements with smooth animations
- **Mobile-First**: Optimized for mobile devices
- **Accessibility**: High contrast and readable fonts

## 🔧 Configuration

### Database Settings

Edit `quitescan/settings.py` to configure your database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'quitescan_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Static Files

For production, configure static files:

```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

## 📊 API Endpoints

- `GET /` - Landing page
- `GET /admin/dashboard/` - Admin dashboard
- `GET /admin/register-student/` - Student registration form
- `GET /admin/students/` - Student list
- `GET /admin/report/` - Attendance reports
- `GET /student/scan/` - QR scanning page
- `POST /student/process-scan/` - Process QR code scan

## 🛠️ Technologies Used

- **Backend**: Django 4.2.7
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS
- **QR Code**: qrcode library
- **Image Processing**: Pillow
- **QR Scanning**: jsQR library

## 🔒 Security Features

- CSRF protection on all forms
- SQL injection prevention through Django ORM
- XSS protection
- Secure file uploads for QR codes
- Authentication required for admin functions

## 📱 Mobile Features

- Camera access for QR scanning
- Touch-friendly interface
- Responsive design
- Offline-capable scanning
- Progressive Web App ready

## 🚀 Deployment

### Production Setup

1. **Set environment variables**
   ```bash
   export DJANGO_SETTINGS_MODULE=quitescan.settings
   export SECRET_KEY=your-secret-key
   export DEBUG=False
   ```

2. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

3. **Configure web server** (Nginx + Gunicorn recommended)

4. **Set up SSL certificate**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## 🔄 Updates

Stay updated with the latest features and bug fixes by regularly pulling from the main branch.

---

**QUITESCAN** - Making student attendance tracking simple and beautiful! 🎓✨

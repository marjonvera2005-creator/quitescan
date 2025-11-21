# Generated manually to rename Course to Department

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_course_student_address_student_approved_at_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Course',
            new_name='Department',
        ),
        migrations.RenameField(
            model_name='attendancelog',
            old_name='course',
            new_name='department',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='course',
            new_name='department',
        ),
    ]

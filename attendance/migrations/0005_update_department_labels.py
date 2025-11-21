from django.db import migrations


def forwards(apps, schema_editor):
    Department = apps.get_model('attendance', 'Department')

    Department.objects.filter(name__iexact='School of Education').update(name='School of Teacher Education')

    Department.objects.filter(
        name__iexact='CS101-COMPUTER SCIENCE'
    ).delete()
    Department.objects.filter(
        code__iexact='CS101'
    ).delete()


def backwards(apps, schema_editor):
    Department = apps.get_model('attendance', 'Department')

    Department.objects.filter(name__iexact='School of Teacher Education').update(name='School of Education')

    if not Department.objects.filter(code__iexact='CS101').exists():
        Department.objects.create(
            name='CS101-COMPUTER SCIENCE',
            code='CS101',
            description='Computer Science Department',
            is_active=True,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_rename_course_to_department'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]


# Generated manually for course field addition

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='course',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='attendancelog',
            name='course',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]







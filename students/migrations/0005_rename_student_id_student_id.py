# Generated by Django 5.1.5 on 2025-01-21 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_alter_student_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='student_id',
            new_name='id',
        ),
    ]

# Generated by Django 5.0.3 on 2024-04-01 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IDPAPP', '0020_outrecord_homeouting_student_generalouting_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outrecord',
            name='HomeOuting',
        ),
        migrations.RemoveField(
            model_name='student',
            name='GeneralOuting',
        ),
        migrations.RemoveField(
            model_name='student',
            name='HomeOuting',
        ),
    ]

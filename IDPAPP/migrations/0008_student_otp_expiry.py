# Generated by Django 5.0.3 on 2024-03-18 13:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDPAPP', '0007_student_otp_student_uid_outrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='otp_expiry',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

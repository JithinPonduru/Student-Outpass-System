# Generated by Django 3.2.21 on 2024-03-02 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDPAPP', '0004_auto_20240301_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='InTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='OutTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

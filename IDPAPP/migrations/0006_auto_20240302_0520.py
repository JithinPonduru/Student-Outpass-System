# Generated by Django 3.2.21 on 2024-03-02 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDPAPP', '0005_auto_20240302_0516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='InTime',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='OutTime',
            field=models.CharField(max_length=200),
        ),
    ]

# Generated by Django 5.0.3 on 2024-04-01 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDPAPP', '0021_remove_outrecord_homeouting_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='outrecord',
            name='GeneralOuting',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='outrecord',
            name='HomeOuting',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='GeneralOuting',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='student',
            name='HomeOuting',
            field=models.BooleanField(default=False),
        ),
    ]
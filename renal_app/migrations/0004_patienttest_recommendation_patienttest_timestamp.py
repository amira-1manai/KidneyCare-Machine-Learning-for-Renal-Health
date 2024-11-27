# Generated by Django 5.0.3 on 2024-08-23 07:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renal_app', '0003_patienttest_message_patienttest_message_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='patienttest',
            name='recommendation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patienttest',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

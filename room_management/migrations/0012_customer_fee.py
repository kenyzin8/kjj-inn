# Generated by Django 5.0.3 on 2024-03-16 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_management', '0011_customer_plate_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='fee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='room_management.fee'),
        ),
    ]

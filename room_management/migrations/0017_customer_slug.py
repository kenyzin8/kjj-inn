# Generated by Django 5.0.3 on 2024-03-17 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_management', '0016_alter_customer_check_in_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True),
        ),
    ]

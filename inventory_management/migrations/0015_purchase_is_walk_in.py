# Generated by Django 5.0.3 on 2024-03-18 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0014_alter_purchase_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='is_walk_in',
            field=models.BooleanField(default=False),
        ),
    ]

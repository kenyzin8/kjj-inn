# Generated by Django 5.0.3 on 2024-03-17 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0007_alter_stock_expiry_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='stocks',
            new_name='products_bought',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='price',
        ),
    ]

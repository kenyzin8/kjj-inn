# Generated by Django 5.0.3 on 2024-03-18 12:04

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0008_rename_stocks_purchase_products_bought_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='identifier',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]

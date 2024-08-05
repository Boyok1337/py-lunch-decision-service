# Generated by Django 5.0.7 on 2024-08-05 09:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0002_restaurant_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="restaurant",
            name="data",
        ),
        migrations.AddField(
            model_name="menuitem",
            name="data",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
# Generated by Django 4.1.4 on 2022-12-22 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base_models", "0004_alter_scan_related_scans"),
    ]

    operations = [
        migrations.AddField(
            model_name="scan",
            name="is_raw",
            field=models.BooleanField(default=False),
        ),
    ]

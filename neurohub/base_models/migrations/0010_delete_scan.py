# Generated by Django 4.1.4 on 2022-12-25 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base_models", "0009_alter_scan_nifti"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Scan",
        ),
    ]

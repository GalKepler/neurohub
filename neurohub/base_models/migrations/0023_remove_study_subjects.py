# Generated by Django 4.1.4 on 2023-01-04 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base_models", "0022_study"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="study",
            name="subjects",
        ),
    ]

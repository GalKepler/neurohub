# Generated by Django 4.1.4 on 2022-12-25 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base_models", "0017_subject"),
    ]

    operations = [
        migrations.RenameField(
            model_name="subject",
            old_name="id_number",
            new_name="pylabber_id",
        ),
    ]
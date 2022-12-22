# Generated by Django 4.1.4 on 2022-12-22 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Scan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nifti_path", models.CharField(max_length=255)),
                ("json_path", models.CharField(max_length=255, null=True)),
            ],
            options={
                "verbose_name": "Scan",
                "verbose_name_plural": "Scans",
            },
        ),
    ]

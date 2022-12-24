# Generated by Django 4.1.4 on 2022-12-24 12:20

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("base_models", "0005_scan_is_raw"),
    ]

    operations = [
        migrations.CreateModel(
            name="NIfTI",
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
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("path", models.FilePathField(max_length=1000, unique=True)),
                ("is_raw", models.BooleanField(default=False)),
                (
                    "parent",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="derivative_set",
                        to="base_models.nifti",
                    ),
                ),
            ],
            options={
                "verbose_name": "NIfTI",
                "ordering": ("-id",),
            },
        ),
    ]

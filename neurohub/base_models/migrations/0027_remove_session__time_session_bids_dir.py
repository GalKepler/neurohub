# Generated by Django 4.1.4 on 2023-01-05 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "base_models",
            "0026_tensorderivative_acquisition_tensorderivative_atlas_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="session",
            name="_time",
        ),
        migrations.AddField(
            model_name="session",
            name="bids_dir",
            field=models.CharField(default=0, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.1.4 on 2023-01-08 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base_models", "0032_alter_tensorderivative_session"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tensorderivative",
            name="session",
        ),
        migrations.AddField(
            model_name="tensorderivative",
            name="session_parent",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tensor_derivatives_set",
                to="base_models.session",
            ),
        ),
    ]

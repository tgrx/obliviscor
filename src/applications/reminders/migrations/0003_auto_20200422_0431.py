# Generated by Django 3.0.5 on 2020-04-22 01:31

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("reminders", "0002_auto_20200420_1205"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reminder",
            name="status",
            field=models.CharField(
                choices=[
                    ("CREATED", "Created"),
                    ("DONE", "Done"),
                    ("ENQUEUED", "Enqueued"),
                    ("NOTIFIED", "Notified"),
                ],
                default="CREATED",
                max_length=255,
            ),
        ),
    ]
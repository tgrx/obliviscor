# Generated by Django 3.0.5 on 2020-04-20 12:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("reminders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reminder",
            name="creator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="own_reminders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

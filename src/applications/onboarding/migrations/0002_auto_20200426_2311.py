# Generated by Django 3.0.5 on 2020-04-26 20:11

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("onboarding", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="authprofile",
            name="notified_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="authprofile",
            name="site",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="sites.Site",
            ),
        ),
    ]

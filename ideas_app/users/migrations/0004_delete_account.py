# Generated by Django 5.1.5 on 2025-01-31 10:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_account"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Account",
        ),
    ]

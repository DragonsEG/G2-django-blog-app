# Generated by Django 4.2.5 on 2023-10-09 03:33

import django.contrib.postgres.fields
from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="companyprofile",
            name="contacts",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=phonenumber_field.modelfields.PhoneNumberField(
                    blank=True, max_length=20, null=True, region=None
                ),
                size=4,
            ),
        ),
    ]

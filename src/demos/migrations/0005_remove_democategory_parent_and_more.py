# Generated by Django 5.0.2 on 2025-01-15 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("demos", "0004_democategory_sub_parent_alter_democategory_parent"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="democategory",
            name="parent",
        ),
        migrations.RemoveField(
            model_name="democategory",
            name="sub_parent",
        ),
    ]

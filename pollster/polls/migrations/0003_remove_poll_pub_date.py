# Generated by Django 4.2.9 on 2024-02-04 15:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0002_choice_created_at_choice_updated_at_poll_created_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="poll",
            name="pub_date",
        ),
    ]
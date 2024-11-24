# Generated by Django 5.1.3 on 2024-11-18 09:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Badge",
            fields=[
                ("id_badge", models.IntegerField(primary_key=True, serialize=False)),
                ("nom", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
            ],
        ),
    ]
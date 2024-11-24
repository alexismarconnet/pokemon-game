# Generated by Django 5.1.3 on 2024-11-17 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("blog", "0002_delete_character_delete_equipement"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lieu",
            fields=[
                (
                    "id_lieu",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("disponibilite", models.CharField(max_length=20)),
                ("photo", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Character",
            fields=[
                (
                    "id_character",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("etat", models.CharField(max_length=20)),
                ("type", models.CharField(max_length=20)),
                ("team", models.CharField(max_length=20)),
                ("photo", models.CharField(max_length=200)),
                (
                    "lieu",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.lieu"
                    ),
                ),
            ],
        ),
    ]

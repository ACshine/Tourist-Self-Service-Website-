# Generated by Django 4.2.13 on 2024-07-09 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Attraction", "0004_alter_attraction_official_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="attraction",
            name="search_count",
            field=models.IntegerField(default=0, verbose_name="搜索次数"),
        ),
    ]

# Generated by Django 4.2.13 on 2024-07-09 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Attraction", "0005_attraction_search_count"),
    ]

    operations = [
        migrations.RemoveField(model_name="comment", name="optional_image",),
        migrations.CreateModel(
            name="CommentImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to="comment_images/", verbose_name="评论图片"),
                ),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="Attraction.comment",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AttractionImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="attraction_images/", verbose_name="景点图片"
                    ),
                ),
                (
                    "attraction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="Attraction.attraction",
                    ),
                ),
            ],
        ),
    ]

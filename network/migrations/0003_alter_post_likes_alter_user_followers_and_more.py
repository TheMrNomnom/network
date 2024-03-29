# Generated by Django 4.2.4 on 2023-08-07 18:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0002_user_followers_user_following_post"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                default=None, related_name="likes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="followers",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="user_followers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="following",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="user_following",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

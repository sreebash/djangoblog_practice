# Generated by Django 2.2 on 2019-04-11 11:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_article_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='profile_picture',
            field=models.FileField(default=datetime.datetime(2019, 4, 11, 11, 22, 42, 194710, tzinfo=utc), upload_to=''),
            preserve_default=False,
        ),
    ]
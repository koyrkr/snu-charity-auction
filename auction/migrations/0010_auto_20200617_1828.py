# Generated by Django 3.0.7 on 2020-06-17 09:28

import auction.models
from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0009_auto_20200617_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='image2',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to=auction.models.image_path2),
        ),
        migrations.AddField(
            model_name='auction',
            name='image3',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to=auction.models.image_path3),
        ),
    ]

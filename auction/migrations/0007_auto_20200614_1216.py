# Generated by Django 3.0.7 on 2020-06-14 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0006_merge_20200614_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='deleted_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='deleted_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
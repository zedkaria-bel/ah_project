# Generated by Django 3.2 on 2021-07-13 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0150_auto_20210712_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='bag_suivi',
            name='match',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]

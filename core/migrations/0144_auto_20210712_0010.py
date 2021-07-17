# Generated by Django 3.2 on 2021-07-12 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0143_alter_bag_suivi_accord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bag_suivi',
            name='obs',
        ),
        migrations.AddField(
            model_name='bag_details',
            name='obs',
            field=models.TextField(blank=True, db_column='OBS', null=True),
        ),
        migrations.AddField(
            model_name='bag_suivi',
            name='rmq',
            field=models.TextField(blank=True, db_column='RMQ', null=True),
        ),
    ]
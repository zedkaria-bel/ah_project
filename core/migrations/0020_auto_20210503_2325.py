# Generated by Django 3.2 on 2021-05-03 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20210503_2235'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CHG_FI',
        ),
        migrations.DeleteModel(
            name='CHG_SSIM',
        ),
        migrations.DeleteModel(
            name='COMP_DISPATCHER',
        ),
        migrations.DeleteModel(
            name='FLIGHT_FI',
        ),
        migrations.DeleteModel(
            name='FLIGHT_OCCAS',
        ),
        migrations.DeleteModel(
            name='FLIGHT_SSIM',
        ),
    ]

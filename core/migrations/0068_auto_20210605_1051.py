# Generated by Django 3.2 on 2021-06-05 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0067_tarif_occas'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarif_occas',
            name='date_last_edit',
            field=models.DateTimeField(auto_now=True, db_column='DATE LAST EDIT', null=True),
        ),
        migrations.AddField(
            model_name='tarif_occas',
            name='user_last_edit',
            field=models.TextField(blank=True, db_column='USER LAST EDIT', null=True),
        ),
    ]

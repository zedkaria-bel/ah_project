# Generated by Django 3.2 on 2021-05-25 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_auto_20210525_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='comp_dispatcher',
            name='user_last_edit',
            field=models.TextField(blank=True, db_column='USER LAST EDIT', null=True),
        ),
    ]

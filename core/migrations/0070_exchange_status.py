# Generated by Django 3.2 on 2021-06-05 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_exchange'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='status',
            field=models.TextField(db_column='STATUS', null=True),
        ),
    ]

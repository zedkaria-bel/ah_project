# Generated by Django 3.2 on 2021-06-05 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_auto_20210605_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='EXCHANGE',
            fields=[
                ('auto_id', models.AutoField(primary_key=True, serialize=False)),
                ('usd', models.FloatField(db_column='USD', null=None)),
                ('dzd', models.FloatField(db_column='DZD', null=None)),
                ('eur', models.FloatField(db_column='EUR', null=None)),
                ('user_last_edit', models.TextField(blank=True, db_column='USER LAST EDIT', null=True)),
                ('date_last_edit', models.DateTimeField(auto_now=True, db_column='DATE LAST EDIT', null=True)),
            ],
            options={
                'db_table': 'EXCHANGE',
            },
        ),
    ]
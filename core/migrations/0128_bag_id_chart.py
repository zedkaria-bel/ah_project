# Generated by Django 3.2 on 2021-07-04 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0127_delete_bag_id_chart'),
    ]

    operations = [
        migrations.CreateModel(
            name='BAG_ID_CHART',
            fields=[
                ('code', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.TextField(blank=True, db_column='LABEL', null=True)),
                ('sub_cat', models.TextField(blank=True, db_column='SUB_CAT', null=True)),
                ('cat', models.TextField(blank=True, db_column='CAT', null=True)),
            ],
            options={
                'db_table': 'BAG_ID_CHART',
            },
        ),
    ]

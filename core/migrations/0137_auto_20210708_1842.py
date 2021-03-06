# Generated by Django 3.2 on 2021-07-08 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0136_auto_20210708_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bag_suivi',
            name='bag_brand',
        ),
        migrations.RemoveField(
            model_name='bag_suivi',
            name='bag_details',
        ),
        migrations.RemoveField(
            model_name='bag_suivi',
            name='bag_dmg_mrd',
        ),
        migrations.RemoveField(
            model_name='bag_suivi',
            name='bag_id',
        ),
        migrations.RemoveField(
            model_name='bag_suivi',
            name='bag_phone',
        ),
        migrations.RemoveField(
            model_name='bag_suivi',
            name='bag_weight',
        ),
        migrations.RemoveField(
            model_name='bag_suivi',
            name='content_dmg',
        ),
        migrations.RemoveField(
            model_name='bag_suivi',
            name='etkt',
        ),
        migrations.RemoveField(
            model_name='bag_suivi',
            name='n_tag',
        ),
        migrations.CreateModel(
            name='BAG_DETAILS',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('bag_weight', models.FloatField(blank=True, db_column='WEIGHT', null=True)),
                ('bag_brand', models.TextField(blank=True, db_column='BRAND NAME', null=True)),
                ('bag_details', models.TextField(blank=True, db_column='DETAILS', null=True)),
                ('bag_phone', models.CharField(blank=True, db_column='PHONE ON BAG', max_length=10, null=True)),
                ('bag_id', models.TextField(blank=True, db_column='BAG ID', null=True)),
                ('content_dmg', models.TextField(blank=True, db_column='CONTENT DMG', null=True)),
                ('bag_dmg_mrd', models.TextField(blank=True, db_column='BAG DMG ID MRD', null=True)),
                ('n_tag', models.PositiveIntegerField(blank=True, db_column='TAG', null=True)),
                ('etkt', models.PositiveIntegerField(blank=True, db_column='ETKT', null=True)),
                ('suivi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.bag_suivi')),
            ],
            options={
                'db_table': 'BAG_DETAILS',
            },
        ),
    ]

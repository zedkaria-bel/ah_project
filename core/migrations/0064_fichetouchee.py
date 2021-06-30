# Generated by Django 3.2 on 2021-06-03 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_auto_20210601_1500'),
    ]

    operations = [
        migrations.CreateModel(
            name='FicheTouchee',
            fields=[
                ('n_fiche', models.IntegerField(db_column='N° FICHE', primary_key=True, serialize=False)),
                ('status', models.TextField(blank=True, db_column='STATUS', null=True)),
                ('key_flt', models.ForeignKey(blank=True, db_column='KEY_FLT', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.flight_assist')),
            ],
            options={
                'db_table': 'FICHE_TOUCHEE',
            },
        ),
    ]

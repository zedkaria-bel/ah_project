# Generated by Django 3.2 on 2021-06-24 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0101_delete_historique_regular_fact'),
    ]

    operations = [
        migrations.CreateModel(
            name='HISTORIQUE_REGULAR_FACT',
            fields=[
                ('date_last_add', models.DateTimeField(auto_now=True, db_column='DATE LAST ADD', primary_key=True, serialize=False)),
                ('from_date', models.DateField(blank=True, db_column='FROM', null=True)),
                ('until_date', models.DateField(blank=True, db_column='UNTIL', null=True)),
                ('montant', models.FloatField(blank=True, db_column='MONTANT', null=True)),
                ('company', models.ForeignKey(blank=True, db_column='COMPANY', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.comp_dispatcher')),
            ],
            options={
                'db_table': 'HISTORIQUE_REGULAR_FACT',
            },
        ),
    ]
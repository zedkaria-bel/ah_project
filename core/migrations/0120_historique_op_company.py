# Generated by Django 3.2 on 2021-07-01 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0119_historique_regular_fact_type_fact'),
    ]

    operations = [
        migrations.CreateModel(
            name='HISTORIQUE_OP_COMPANY',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_last_add', models.DateTimeField(auto_now=True, db_column='DATE LAST ADD', null=True)),
                ('old_solde', models.FloatField(blank=True, db_column='OLD_SOLDE', null=True)),
                ('date_old_solde', models.DateField(blank=True, db_column='OLD SOLDE DATE', null=True)),
                ('date_new_solde', models.DateField(blank=True, db_column='NEW SOLDE DATE', null=True)),
                ('new_solde', models.FloatField(blank=True, db_column='NEW_SOLDE', null=True)),
                ('company', models.ForeignKey(blank=True, db_column='COMPANY', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.comp_dispatcher')),
                ('user_add', models.ForeignKey(blank=True, db_column='USER', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'HISTORIQUE_OP_COMPANY',
            },
        ),
    ]
# Generated by Django 3.2 on 2021-06-10 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0088_auto_20210610_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fiche_touchee',
            name='cnl_cause_fiche',
            field=models.TextField(blank=True, db_column='CAUSE CNL FICHE', null=True),
        ),
    ]

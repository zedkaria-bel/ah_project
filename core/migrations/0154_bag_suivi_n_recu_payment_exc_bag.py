# Generated by Django 3.2 on 2021-07-14 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0153_auto_20210713_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='bag_suivi',
            name='n_recu_payment_exc_bag',
            field=models.TextField(blank=True, db_column='N REF PAYMENT EXC BAG', null=True),
        ),
    ]

# Generated by Django 4.0.1 on 2022-04-06 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_bond_ispurchased'),
    ]

    operations = [
        migrations.AddField(
            model_name='bond',
            name='priceInUSD',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=13, null=True),
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-10 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.FloatField(null=True),
        ),
    ]

# Generated by Django 2.1.7 on 2019-04-05 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wheredoyoulive', '0004_auto_20190404_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='address',
            field=models.CharField(default='180 Main Street, Andover, MA', max_length=100),
            preserve_default=False,
        ),
    ]
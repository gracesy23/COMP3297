# Generated by Django 2.1.7 on 2019-04-26 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20190426_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='courset',
            name='autobio',
            field=models.CharField(default='N/A', max_length=200),
        ),
    ]

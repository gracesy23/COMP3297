# Generated by Django 2.1.7 on 2019-04-26 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20190426_0749'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='entry', max_length=200)),
                ('compID', models.IntegerField()),
                ('content', models.TextField(max_length=200)),
                ('componentType', models.IntegerField(default='1')),
                ('used', models.IntegerField(default='0')),
                ('place', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='component',
            name='place',
        ),
        migrations.AddField(
            model_name='component',
            name='courseID',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='courseID',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quiz',
            name='standard',
            field=models.IntegerField(default=60),
        ),
    ]

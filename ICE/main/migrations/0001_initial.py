# Generated by Django 2.1.7 on 2019-04-08 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compID', models.IntegerField()),
                ('content', models.TextField(max_length=200)),
                ('componentType', models.IntegerField(default='1')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseID', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('created_by', models.IntegerField()),
                ('contains_modules', models.IntegerField()),
                ('description', models.TextField(default='N/A', max_length=200)),
                ('category', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CourseT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseID', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=200)),
                ('taught_by', models.CharField(max_length=200)),
                ('enroll', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instructorID', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('create_course', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Learner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learnerID', models.IntegerField()),
                ('learnerName', models.CharField(max_length=200)),
                ('takecourse', models.IntegerField()),
                ('progress', models.IntegerField()),
                ('pass_date', models.DateField(default='2000-01-01')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moduleID', models.IntegerField()),
                ('moduleTitle', models.CharField(max_length=200)),
                ('containsComp', models.IntegerField()),
                ('containsQuiz', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ModuleT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modID', models.IntegerField()),
                ('title', models.CharField(default='unnamed', max_length=200)),
                ('counter', models.IntegerField(default='1')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionID', models.IntegerField()),
                ('question', models.TextField(max_length=200)),
                ('choiceA', models.TextField(max_length=200)),
                ('choiceB', models.TextField(max_length=200)),
                ('choiceC', models.TextField(max_length=200)),
                ('choiceD', models.TextField(max_length=200)),
                ('answer', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quizID', models.IntegerField()),
                ('questionID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='QuizT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quizID', models.IntegerField()),
                ('numOfQuestion', models.IntegerField(default='0')),
            ],
        ),
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseID', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('progress', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserLogin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('role', models.IntegerField()),
                ('userID', models.IntegerField()),
            ],
        ),
    ]

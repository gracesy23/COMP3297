from django.db import models

# Create your models here.
class Course(models.Model):
	courseID = models.IntegerField()
	title = models.CharField(max_length = 200)
	created_by = models.IntegerField()
	contains_modules = models.IntegerField()
	
class Learner(models.Model):
	learnerID = models.IntegerField()
	learnerName = models.CharField(max_length = 200)
	takecourse = models.IntegerField()
	progress = models.IntegerField()

class Module(models.Model):
	moduleID = models.IntegerField()
	moduleTitle = models.CharField(max_length = 200)
	containsComp = models.IntegerField()
	containsQuiz = models.IntegerField()
	
class Component(models.Model):
	compID = models.IntegerField()
	content = models.TextField(max_length = 200)
	componentType = models.IntegerField(default='1')
	
class Quiz(models.Model):
	quizID = models.IntegerField()
	questionID = models.IntegerField()

class QuizT(models.Model):
	quizID = models.IntegerField()
	numOfQuestion = models.IntegerField(default='0')
	
class Temp(models.Model):
	courseID = models.IntegerField()
	title = models.CharField(max_length = 200)
	progress = models.IntegerField()
	
class ModuleT(models.Model):
	modID = models.IntegerField()
	title = models.CharField(max_length = 200, default='unnamed')
	counter = models.IntegerField(default='1')
	
class Question(models.Model):
	questionID = models.IntegerField()
	question = models.TextField(max_length = 200)
	choiceA = models.TextField(max_length = 200)
	choiceB = models.TextField(max_length = 200)
	choiceC = models.TextField(max_length = 200)
	choiceD = models.TextField(max_length = 200)
	answer = models.CharField(max_length = 200)
	
	
	
	
	
	
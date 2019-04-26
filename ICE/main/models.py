from django.db import models

# Create your models here.

class InstructorInfo(models.Model):
	instructorID = models.IntegerField()
	first_name = models.CharField(max_length = 200)
	last_name = models.CharField(max_length = 200)
	intro = models.TextField(max_length = 200)

class Category(models.Model):
	cateID = models.IntegerField()
	title = models.CharField(max_length = 200)

class Staff(models.Model):
	staffID = models.IntegerField()
	email = models.CharField(max_length = 200)
	first_name = models.CharField(max_length = 200)
	last_name = models.CharField(max_length = 200)
	
class Token(models.Model):
	token = models.IntegerField()
	role = models.IntegerField()
	staffID = models.IntegerField()

class UserLogin(models.Model):
	username = models.CharField(max_length = 200)
	role = models.IntegerField()
	userID = models.IntegerField()
	
class Course(models.Model):
	courseID = models.IntegerField()
	CECU = models.IntegerField(default = 6)
	title = models.CharField(max_length = 200)
	created_by = models.IntegerField()
	contains_modules = models.IntegerField()
	description = models.TextField(max_length = 200,default = "N/A")
	category = models.IntegerField(default = 0)

class Learner(models.Model):
	learnerID = models.IntegerField()
	email = models.CharField(max_length = 200)
	first_name = models.CharField(max_length = 200)
	last_name = models.CharField(max_length = 200)
	
class Progress(models.Model):
	learnerID = models.IntegerField()
	takecourse = models.IntegerField()
	progress = models.IntegerField()
	pass_date = models.DateField(default="2000-01-01")
	learnerName = models.CharField(max_length = 200)

class Module(models.Model):
	moduleID = models.IntegerField()
	moduleTitle = models.CharField(max_length = 200)
	containsComp = models.IntegerField()
	containsQuiz = models.IntegerField()
	
class Component(models.Model):
	title = models.CharField(max_length = 200,default = 'entry')
	compID = models.IntegerField()
	content = models.TextField(max_length = 200)
	componentType = models.IntegerField(default='1')
	used = models.IntegerField(default='0')
	
class ComponentT(models.Model):
	title = models.CharField(max_length = 200,default = 'entry')
	compID = models.IntegerField()
	content = models.TextField(max_length = 200)
	componentType = models.IntegerField(default='1')
	used = models.IntegerField(default='0')
	place = models.IntegerField(default = 0)
	
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
	pass_date = models.DateField(default = '2000-01-01')
	category = models.CharField(max_length = 200,default = 'N/A')
	description = models.TextField(default = 'N/A')
	
class ModuleT(models.Model):
	modID = models.IntegerField()
	title = models.CharField(max_length = 200, default='unnamed')
	counter = models.IntegerField(default='1')
	place = models.IntegerField(default = '0')
	
class Question(models.Model):
	questionID = models.IntegerField()
	question = models.TextField(max_length = 200)
	choiceA = models.TextField(max_length = 200)
	choiceB = models.TextField(max_length = 200)
	choiceC = models.TextField(max_length = 200)
	choiceD = models.TextField(max_length = 200)
	answer = models.CharField(max_length = 200)
	
class Instructor(models.Model):
	instructorID = models.IntegerField()
	name = models.CharField(max_length = 200)
	create_course = models.IntegerField()

class CourseT(models.Model):
	courseID = models.IntegerField()
	title = models.CharField(max_length = 200)
	description = models.TextField(max_length = 200)
	taught_by = models.CharField(max_length = 200)
	enroll = models.IntegerField()
	CECU = models.IntegerField(default=6)
	
class History(models.Model):
	title = models.CharField(max_length = 200)
	date = models.DateField(default="2000-01-01")
	CECU = models.IntegerField()
	CCECU = models.IntegerField()
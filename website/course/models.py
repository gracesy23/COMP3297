from django.db import models
from django.urls import reverse
# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    type = models.CharField(max_length=200)
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('course:detail', kwargs={'pk': self.pk})
    def __str__(self):
        return self.name + ' - ' + self.instructor

class Module(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    have_quiz = models.BooleanField(default=False)
    is_select = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse('course:module', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class Component(models.Model):
    CATEGORY_CHOICES={
        ('text', 'text'),
        ('image', 'image'),
    }
    name = name = models.CharField(max_length=200, default="")
    text = models.TextField(blank=True)
    image = models.FileField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='text')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_select = models.BooleanField(default=False)
    module_id = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    passRequire = models.PositiveIntegerField()
    is_select = models.BooleanField(default=False)
    module_id = models.IntegerField(blank=True, default=0)
    def __str__(self):
        return self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    def __str__(self):
        return self.question + ' - ' + self.quiz.name

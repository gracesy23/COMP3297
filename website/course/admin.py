from django.contrib import admin

# Register your models here.
from .models import Course, Component, Module, Question, Quiz
admin.site.register(Course)
admin.site.register(Component)
admin.site.register(Module)
admin.site.register(Quiz)
admin.site.register(Question)

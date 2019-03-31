from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^learner/(?P<id>\d)/$', views.learner, name = 'learner'),
	url(r'^instructor/(?P<iid>\d)/(?P<cid>\d)/$', views.instructor, name = 'instructor'),
	url(r'^instructor/course/module/(?P<mid>\d)/$', views.changeModName, name = 'changemodname'),
	url(r'^instructor/course/module/addComp/(?P<mid>\d)/$', views.addComp, name = 'addComp'),
	url(r'^instructor/course/module/addQuiz/(?P<mid>\d)/$', views.addQuiz, name = 'addQuiz'),
	url(r'^instructor/course/module/(?P<mid>\d)/$', views.moduleIns, name = 'moduleIns'),
	url(r'^instructor/course/(?P<cid>\d)/(?P<iid>\d)/$', views.createModule, name = 'moduleCreate'),
	path('instructor', views.instructor, name = 'instructor'),
	url('learner/course/(?P<p>\d)/(?P<cid>\d)/(?P<lid>\d)/$', views.course, name = 'course'),
	url('learner/course/module/(?P<mid>\d)/(?P<cid>\d)/(?P<p>\d)/(?P<lid>\d)/$', views.module, name = 'module'),
	url('learner/course/module/quiz/(?P<qid>\d)/(?P<cid>\d)/(?P<p>\d)/(?P<lid>\d)', views.quiz, name = 'quiz'),
]
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^learner/(?P<id>\d)/$', views.learner, name = 'learner'),
	url(r'^instructor/(?P<iid>\d)/(?P<cid>\d)/$', views.instructor, name = 'instructor'),
	url(r'^instructor/course/module/(?P<mid>\d)/(?P<iid>\d)/(?P<cid>\d)/$', views.changeModName, name = 'changemodname'),
	url(r'^instructor/course/module/addComp/(?P<mid>\d)/(?P<iid>\d)/(?P<cid>\d)/$', views.addComp, name = 'addComp'),
	url(r'^instructor/course/module/addQuiz/(?P<mid>\d)/(?P<iid>\d)/(?P<cid>\d)/$', views.addQuiz, name = 'addQuiz'),
	url(r'^instructor/course/module/(?P<mid>\d)/(?P<iid>\d)/(?P<cid>\d)/$', views.moduleIns, name = 'moduleIns'),
	url(r'^instructor/course/(?P<cid>\d)/(?P<iid>\d)/$', views.createModule, name = 'moduleCreate'),
    url(r'^learner/coursemod/loadComp/', views.loadComp, name='loadComp'),	
	path('instructor', views.instructor, name = 'instructor'),
	url('learner/course/(?P<p>\d)/(?P<cid>\d)/(?P<lid>\d)/$', views.course, name = 'course'),
	url('learner/course/module/(?P<mid>\d)/(?P<cid>\d)/(?P<p>\d)/(?P<lid>\d)/(?P<counter>\d)/$', views.module, name = 'module'),
	url('learner/coursemod/(?P<p>\d)/(?P<cid>\d)/(?P<lid>\d)/(?P<mid>\d)/(?P<counter>\d)/$', views.courseModule, name = 'courseModule'),
	url('learner/course/module/quiz/(?P<qid>\d)/(?P<cid>\d)/(?P<p>\d)/(?P<lid>\d)', views.quiz, name = 'quiz'),
]
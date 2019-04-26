from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('learnersignup/', views.learner_signup, name='learner_signup'),
	url(r'^signup/(?P<token>\d+)/$', views.SignUp.as_view(), name='signup'),
	path('newaccount', views.newaccount, name='newaccount'),
	url(r'^account/confirm/instructor/(?P<iid>\d+)/$', views.instructor_reg_sup, name='instructor_reg_sup'),
	url(r'^account/confirm/(?P<token>\w+)/(?P<username>\w+)/$', views.newaccount_sup, name='registrate'),
	url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
	url(r'^redirect/$', views.redirect),
	url(r'^loggedout/$', views.loggedout),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
	url(r'^learner/history/(?P<lid>\d+)/$', views.viewlist, name = 'view_history'),
	url(r'^learner/(?P<id>\d+)/$', views.learner, name = 'learner'),
	url('instructor/changemodorder/(?P<iid>\d+)/(?P<cid>\d+)/$', views.change_mod_order, name = 'change_mod_order'),
	url('instructor/changecomporder/(?P<mid>\d+)/(?P<iid>\d+)/(?P<cid>\d+)/$', views.change_comp_order, name = 'change_comp_order'),
	url(r'^instructor/create/(?P<iid>\d+)/$', views.create_new_course, name = 'create_new_course'),
	url(r'^instructor/(?P<iid>\d+)/$', views.instructorHome, name = 'instructorHome'),
	url(r'^instructor/(?P<iid>\d+)/(?P<cid>\d+)/$', views.instructor, name = 'instructor'),
	url(r'^instructor/course/module/(?P<mid>\d+)/(?P<iid>\d+)/(?P<cid>\d+)/$', views.changeModName, name = 'changemodname'),
	url(r'^instructor/course/module/addComp/(?P<mid>\d+)/(?P<iid>\d+)/(?P<cid>\d+)/$', views.addComp, name = 'addComp'),
	url(r'^instructor/course/module/addQuiz/(?P<mid>\d+)/(?P<iid>\d+)/(?P<cid>\d+)/$', views.addQuiz, name = 'addQuiz'),
	url(r'^instructor/course/module/(?P<mid>\d+)/(?P<iid>\d+)/(?P<cid>\d+)/$', views.moduleIns, name = 'moduleIns'),
	url(r'^instructor/course/(?P<cid>\d+)/(?P<iid>\d+)/$', views.createModule, name = 'moduleCreate'),
    url(r'^learner/coursemod/loadComp/', views.loadComp, name='loadComp'),	
	url(r'instructor', views.instructor, name = 'instructor'),
	url(r'sendmail', views.sendmail, name = 'sendmail'),
	url('learner/course/(?P<p>\d+)/(?P<cid>\d+)/(?P<lid>\d+)/$', views.course, name = 'course'),
	url('learner/course/module/(?P<mid>\d+)/(?P<cid>\d+)/(?P<p>\d+)/(?P<lid>\d+)/(?P<counter>\d+)/$', views.module, name = 'module'),
	url('learner/coursemod/(?P<p>\d+)/(?P<cid>\d+)/(?P<lid>\d+)/(?P<mid>\d+)/(?P<counter>\d+)/$', views.courseModule, name = 'courseModule'),
	url('learner/course/module/quiz/(?P<qid>\d+)/(?P<cid>\d+)/(?P<p>\d+)/(?P<lid>\d+)', views.quiz, name = 'quiz'),
	url('learner/course/module/quiz/check/(?P<qid>\d+)/(?P<cid>\d+)/(?P<p>\d+)/(?P<lid>\d+)', views.quizCheck, name = 'quizcheck'),
	url('learner/allcourses/(?P<lid>\d+)/(?P<cate>\d+)/(?P<alert>\d+)/$', views.view_all_courses, name = 'allcourses'),
	url('learner/enroll/(?P<lid>\d+)/(?P<cid>\d+)/$', views.enroll, name = 'enroll'),
]
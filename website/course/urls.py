from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    # /course/
    path('', views.CourseView.as_view(), name='index'),

    # /course/<course_id>/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    path('module/<int:pk>/', views.ModuleView.as_view(), name='module'),

    path('module/addCom/<int:pk>/', views.AddCom, name='addCom'),
    path('module/addQuiz/<int:pk>/', views.addQuiz, name='addQuiz'),

    path('<int:pk>/CreateModule/', views.ModuleCreate.as_view(), name='Module-add'),



    path('course/add/', views.CourseCreate.as_view(), name='Course-add'),

]

from django.urls import path
from . import views

urlpatterns =[
    path('home', views.home, name='home'),

    # CRUD 
    path('create-course', views.createCourse , name=' createCourse'),
    path('create-lesson', views.createLesson , name=' createLesson'),
    path('create-subscription', views.createSubscription , name=' createSubscription'),

    # readall
    path('read-courses', views.readCourses, name='readCourses'),
    path('read-lessons', views.readLessons, name='readLessons'),
    path('read-subscriptions', views.readSubscriptions, name='readSubscriptions'),

    # read one
    path('read-courses/<str:pk>', views.readOneCourse, name='readOneCourse'),
    path('read-lessons/<str:pk>', views.readOneLesson, name='readOneLesson'),
    path('read-subscriptions/<str:pk>', views.readOneSubscription, name='readOneSubscription'),
]
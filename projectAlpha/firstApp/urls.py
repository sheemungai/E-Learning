from django.urls import path
from . import views

urlpatterns =[
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('courses', views.courses, name='courses'),
    path('contact', views.contact, name='contact'),
    path('course-lessons/<str:pk>', views.courseLessons, name='courseLessons'),
    path('mpesaPayment', views.mpesaPayment, name='mpesaPayment'),


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

    # update one
    path('update-course/<str:pk>', views.updateCourse, name='updateCourse'),
    path('update-lesson/<str:pk>', views.updateLesson, name='updateLesson'),
    path('update-subscription/<str:pk>', views.updateSubscription, name='updateSubscription'),

    # delete one
    path('delete-course/<str:pk>', views.deleteCourse, name='deleteCourse'),
    path('delete-lesson/<str:pk>', views.deleteLesson, name='deleteLesson'),
    path('delete-subscription/<str:pk>', views.deleteSubscription, name='deleteSubscription'),  
]
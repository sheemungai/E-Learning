from django.shortcuts import render, redirect
from . forms import CourseForm, LessonForm, SubscriptionForm
from . models import Course, Lesson, Subscription

# Create your views here.
def home(request):
    context={}
    return render(request, 'firstApp/home.html', context)


def createCourse(request):
    form = CourseForm()

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form' : form}
    return render(request,'firstApp/form.html' ,context)

def createLesson(request):
    form = LessonForm()

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form' : form}
    return render(request,'firstApp/form.html' ,context)


def createSubscription(request):

    form = SubscriptionForm()

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form' : form}
    return render(request,'firstApp/form.html' ,context)

# readall
def readCourses(request):
    courses = Course.objects.all()
    context ={'data':courses}
    return render(request, 'firstApp/home.html', context)

def readLessons(request):
    lessons = Lesson.objects.all()
    context ={'data':lessons}
    return render(request, 'firstApp/home.html', context)

def readSubscriptions(request):
    subscriptions = Subscription.objects.all()
    context ={'data':subscriptions}
    return render(request, 'firstApp/home.html', context)

# readone
def readOneCourse(request, pk):
    course = Course.objects.get(id=pk)
    context ={'item':course}
    return render(request, 'firstApp/item.html', context)

def readOneLesson(request, pk):
    lesson = Lesson.objects.get(id=pk)
    context ={'item':lesson}
    return render(request, 'firstApp/item.html', context)

def readOneSubscription(request, pk):
    subscription = Subscription.objects.get(id=pk)
    context ={'item':subscription}
    return render(request, 'firstApp/item.html', context)
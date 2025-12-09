from urllib import request, response
from django.shortcuts import render, redirect
from . forms import CourseForm, LessonForm, SubscriptionForm
from . models import Course, Lesson, Subscription
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient

# Create your views here.
def home(request):
    context={}
    return render(request, 'firstApp/home.html', context)

def about(request):
    context={}
    return render(request, 'firstApp/about.html', context)

def courses(request):
    courses = Course.objects.all()
    context={'courses': courses}
    return render(request, 'firstApp/courses.html', context)

def contact(request):
    context={}
    return render(request, 'firstApp/contact.html', context)

def courseLessons(request, pk):
    course = Course.objects.get(id=pk)
    lessons = course.lessons.all()
    context = {
        'course': course,
        'lessons': lessons
    }
    return render(request, 'firstApp/lessons.html', context)

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
    return render(request, 'firstApp/courses.html', context)

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


#   update one
def updateCourse(request, pk):
    course = Course.objects.get(id=pk)
    form = CourseForm(instance=course)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form' : form}
    return render(request,'firstApp/form.html' ,context)

def updateLesson(request, pk):
    lesson = Lesson.objects.get(id=pk)
    form = LessonForm(instance=lesson)

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form' : form}
    return render(request,'firstApp/form.html' ,context)

def updateSubscription(request, pk):
    subscription = Subscription.objects.get(id=pk)
    form = SubscriptionForm(instance=subscription)

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form' : form}
    return render(request,'firstApp/form.html' ,context)


# delete 
def deleteCourse(request, pk):
    course = Course.objects.get(id=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('home')
    context={'item':course}
    return render(request, 'firstApp/delete.html', context)

def deleteLesson(request, pk):
    lesson = Lesson.objects.get(id=pk)
    if request.method == 'POST':
        lesson.delete()
        return redirect('home')
    context={'item':lesson}
    return render(request, 'firstApp/delete.html', context)

def deleteSubscription(request, pk):
    subscription = Subscription.objects.get(id=pk)
    if request.method == 'POST':
        subscription.delete()
        return redirect('home')
    context={'item':subscription}
    return render(request, 'firstApp/delete.html', context)

# daraja payments

def index(request):
    # cl = MpesaClient()
    # # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    # phone_number = '0701715057'
    # amount = 1
    # account_reference = 'reference'
    # transaction_desc = 'Description'
    # callback_url = 'https://api.darajambili.com/express-payment'
    # response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

def mpesaPayment(request): 
    cl = MpesaClient()
    accountReference = 'courses payment'
    transactionDesc = 'Payment for course enrollment'
    callbackUrl = 'https://api.darajambili.com/express-payment'

    if request.method == 'POST':
        phoneNumber = request.POST.get('phoneNumber')
        amount = request.POST.get('amount')
        
        # Debug: Print to console
        print(f"Phone: {phoneNumber}, Amount: {amount}")
        
        try:
            amount = int(amount)
            response = cl.stk_push(phoneNumber, amount, accountReference, transactionDesc, callbackUrl)
            
            # Show the response
            context = {
                'response': response,
                'success': True,
                'message': 'STK Push sent! Check your phone.'
            }
            print(f"M-Pesa Response: {response}")
            
        except ValueError as e:
            context = {
                'error': f'Invalid amount: {amount}',
                'success': False
            }
            print(f"ValueError: {e}")
            
        except Exception as e:
            context = {
                'error': str(e),
                'success': False,
                'message': 'Failed to send STK push'
            }
            print(f"Error: {e}")
        
        return render(request, 'firstApp/payments.html', context)
    
    # GET request - show form
    context = {}
    return render(request, 'firstApp/payments.html', context)
from urllib import request, response
from django.shortcuts import render, redirect, get_object_or_404
from . forms import CourseForm, LessonForm, SubscriptionForm
from . models import Course, Enrollment, Lesson, Subscription
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from .models import Course, Enrollment, Lesson, Payment
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


# dashboard views

# Check if user is admin/staff
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def userDashboard(request):
    """Student/User Dashboard"""
    user = request.user
    
    # Get user's enrollments
    enrollments = Enrollment.objects.filter(user=user).select_related('course')
    active_enrollments = enrollments.filter(status='active', is_paid=True)
    pending_enrollments = enrollments.filter(status='pending')
    
    # Get user's payments
    from .models import Payment
    payments = Payment.objects.filter(user=user).select_related('course')[:5]
    total_spent = Payment.objects.filter(user=user, status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get available courses
    available_courses = Course.objects.exclude(
        id__in=active_enrollments.values_list('course_id', flat=True)
    )[:4]
    
    # Recent activity
    recent_enrollments = enrollments.order_by('-enrollment_date')[:5]
    
    context = {
        'active_enrollments': active_enrollments,
        'pending_enrollments': pending_enrollments,
        'payments': payments,
        'total_spent': total_spent,
        'available_courses': available_courses,
        'recent_enrollments': recent_enrollments,
        'total_courses': active_enrollments.count(),
        'pending_payments': pending_enrollments.count(),
    }
    return render(request, 'firstApp/user_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def adminDashboard(request):
    """Admin Dashboard"""
    # Overview statistics
    total_courses = Course.objects.count()
    total_lessons = Lesson.objects.count()
    total_students = Enrollment.objects.values('user').distinct().count()
    total_enrollments = Enrollment.objects.count()
    
    # Revenue statistics
    from .models import Payment
    total_revenue = Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    pending_payments = Payment.objects.filter(status='pending').count()
    completed_payments = Payment.objects.filter(status='completed').count()
    
    # Recent activity
    recent_enrollments = Enrollment.objects.select_related('user', 'course').order_by('-enrollment_date')[:10]
    recent_payments = Payment.objects.select_related('user', 'course').order_by('-created_at')[:10]
    
    # Popular courses
    popular_courses = Course.objects.annotate(
        enrollment_count=Count('enrollments')
    ).order_by('-enrollment_count')[:5]
    
    # This month's statistics
    this_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_enrollments = Enrollment.objects.filter(enrollment_date__gte=this_month_start).count()
    monthly_revenue = Payment.objects.filter(
        status='completed',
        payment_date__gte=this_month_start
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Enrollment status breakdown
    active_enrollments = Enrollment.objects.filter(status='active').count()
    pending_enrollments = Enrollment.objects.filter(status='pending').count()
    
    context = {
        'total_courses': total_courses,
        'total_lessons': total_lessons,
        'total_students': total_students,
        'total_enrollments': total_enrollments,
        'total_revenue': total_revenue,
        'pending_payments': pending_payments,
        'completed_payments': completed_payments,
        'recent_enrollments': recent_enrollments,
        'recent_payments': recent_payments,
        'popular_courses': popular_courses,
        'monthly_enrollments': monthly_enrollments,
        'monthly_revenue': monthly_revenue,
        'active_enrollments': active_enrollments,
        'pending_enrollments': pending_enrollments,
    }
    return render(request, 'firstApp/admin_dashboard.html', context)

# Simplified views.py - Add these to your existing views




# ========== ENROLLMENT & PAYMENT ==========

@login_required
def enrollCourse(request, pk):
    """Enroll user in a course"""
    course = get_object_or_404(Course, id=pk)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'status': 'pending', 'is_paid': False, 'payment_required': True}
    )
    
    if enrollment.is_paid:
        messages.info(request, 'You are already enrolled!')
        return redirect('courseLessons', pk=pk)
    
    if created:
        messages.success(request, f'Enrolled! Please complete payment.')
    
    return redirect('coursePayment', enrollment_id=enrollment.id)


@login_required
def coursePayment(request, enrollment_id):
    """Payment page"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, user=request.user)
    
    if enrollment.is_paid:
        return redirect('courseLessons', pk=enrollment.course.id)
    
    if request.method == 'POST':
        phone = request.POST.get('phoneNumber')
        
        # Create payment
        payment = Payment.objects.create(
            enrollment=enrollment,
            user=request.user,
            course=enrollment.course,
            amount=enrollment.course.price,
            phone_number=phone,
            status='pending'
        )
        
        # M-Pesa STK Push
        try:
            cl = MpesaClient()
            response = cl.stk_push(
                phone, 
                int(enrollment.course.price),
                f"ENR-{enrollment.id}",
                f"Payment for {enrollment.course.title}",
                'https://api.darajambili.com/express-payment'
            )
            
            payment.checkout_request_id = response.get('CheckoutRequestID')
            payment.save()
            
            messages.success(request, 'Check your phone for M-Pesa prompt!')
            return redirect('paymentStatus', payment_id=payment.id)
            
        except Exception as e:
            payment.status = 'failed'
            payment.save()
            messages.error(request, f'Payment failed: {str(e)}')
    
    return render(request, 'firstApp/course_payment.html', {
        'enrollment': enrollment,
        'course': enrollment.course
    })


@csrf_exempt
def mpesaCallback(request):
    """M-Pesa callback"""
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        callback = data.get('Body', {}).get('stkCallback', {})
        checkout_id = callback.get('CheckoutRequestID')
        
        try:
            payment = Payment.objects.get(checkout_request_id=checkout_id)
            
            if callback.get('ResultCode') == 0:  # Success
                payment.status = 'completed'
                payment.payment_date = timezone.now()
                payment.save()
                
                # Activate enrollment
                payment.enrollment.is_paid = True
                payment.enrollment.status = 'active'
                payment.enrollment.save()
            else:
                payment.status = 'failed'
                payment.save()
        except:
            pass
        
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid"})


@login_required
def paymentStatus(request, payment_id):
    """Check payment status"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'firstApp/payment_status.html', {
        'payment': payment,
        'enrollment': payment.enrollment,
        'course': payment.course
    })


# ========== PROTECTED LESSONS ==========

@login_required
def courseLessons(request, pk):
    """Only accessible after payment"""
    course = get_object_or_404(Course, id=pk)
    enrollment = Enrollment.objects.filter(
        user=request.user,
        course=course,
        status='active',
        is_paid=True
    ).first()
    
    if not enrollment:
        messages.warning(request, 'Please complete payment to access lessons.')
        return redirect('courses')
    
    return render(request, 'firstApp/lessons.html', {
        'course': course,
        'lessons': course.lessons.all(),
        'enrollment': enrollment
    })


# ========== COURSES WITH ENROLLMENT STATUS ==========

def courses(request):
    """Browse courses"""
    courses = Course.objects.all()
    enrolled_ids = []
    pending_ids = []
    
    if request.user.is_authenticated:
        enrolled_ids = list(Enrollment.objects.filter(
            user=request.user, status='active', is_paid=True
        ).values_list('course_id', flat=True))
        
        pending_ids = list(Enrollment.objects.filter(
            user=request.user, status='pending', is_paid=False
        ).values_list('course_id', flat=True))
    
    return render(request, 'firstApp/courses.html', {
        'courses': courses,
        'enrolled_course_ids': enrolled_ids,
        'pending_payment_course_ids': pending_ids
    })


# ========== USER DASHBOARD ==========

@login_required
def userDashboard(request):
    """Student dashboard"""
    active = Enrollment.objects.filter(
        user=request.user, status='active', is_paid=True
    ).select_related('course')
    
    pending = Enrollment.objects.filter(
        user=request.user, status='pending', is_paid=False
    ).select_related('course')
    
    payments = Payment.objects.filter(
        user=request.user
    ).select_related('course').order_by('-created_at')[:5]
    
    total_spent = Payment.objects.filter(
        user=request.user, status='completed'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    return render(request, 'firstApp/user_dashboard.html', {
        'active_enrollments': active,
        'pending_enrollments': pending,
        'payments': payments,
        'total_spent': total_spent,
        'total_courses': active.count(),
        'pending_payments': pending.count(),
    })
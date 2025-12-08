from django.db import models

# Create your models here.
class Course(models.Model):
    title= models.CharField(max_length=100)
    description= models.CharField(max_length=255)
    category= models.CharField(max_length=200)
    tutor= models.CharField(max_length=100)
    image = models.CharField(max_length=255)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    created_at= models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now=True)


    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons') 
    title= models.CharField(max_length=100)
    description= models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True)
    video_url = models.URLField(blank=True)  # YouTube/Vimeo link OR
    video_file = models.FileField(upload_to='lesson_videos/', blank=True)  # Upload video
    pdf = models.FileField(upload_to='lesson_pdfs/', blank=True)
    duration = models.CharField(max_length=50, blank=True)
    created_at= models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now=True)


    def __str__(self):
        return self.title

class Enrollment(models.Model):
    ENROLLMENT_STATUS = [
        ('pending', 'Pending Payment'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS, default='pending')
    is_paid = models.BooleanField(default=False)
    payment_required = models.BooleanField(default=True)  # False for free courses
    
    class Meta:
        unique_together = ['user', 'course']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.status})"




class Subscription(models.Model):
    PLAN_TYPES = [
        ('free', 'Free'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('lifetime', 'Lifetime'),
    ]
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name



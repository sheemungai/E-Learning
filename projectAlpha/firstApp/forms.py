from django.forms import ModelForm
from . models import Course, Lesson ,Subscription

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'

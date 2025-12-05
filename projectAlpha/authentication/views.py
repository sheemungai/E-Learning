from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.
def loginUser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)

        try:
            user = user.objects.get(username=username)
        except:
            print("User does not exists!")
        
        user = authenticate(request, username= username, password = password)

        if user is not None: 
            login(request, user)
            return redirect('home.html')  #
        else:
            print('Wrong Credentials!!')

    context ={}
    return render(request,'authentication/loginForm.html',context)


def registerUser(request):
    if request.method == 'POST':
        
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        address = request.POST.get('address')
        city = request.POST.get('city')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'authentication/registerForm.html')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return render(request, 'authentication/registerForm.html')

        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'authentication/registerForm.html')

        # Create user
        user = User.objects.create_user(
            username=username.lower(),
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')  
    
    context = {}
    return render(request, 'authentication/registerForm.html', context)


def logoutUser(request):

    logout(request)
    messages.success(request, 'You have been logged out successfully.')  
    return redirect('home')  
   
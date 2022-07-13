from click import password_option
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form_data =  request.POST
        username = form_data['username']
        email = form_data['email']
        password = form_data['password']
        password2 = form_data['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user=  User.objects.create_user(username=username, password=password, email=email)
                '''
                Why prefer User.objects.create_user over User.objects.create ?

                The most significant difference is that if you supply a password to the .create() method, it will be set verbatim on the user, 
                and will not be usable to authenticate the user.

                Instead, the create_user() method hashes the password argument

                refer source: 
                https://github.com/django/django/blob/main/django/contrib/auth/models.py#L145

                '''
                user.save()
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')     
    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
        
    return render(request, 'signin.html')

@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')


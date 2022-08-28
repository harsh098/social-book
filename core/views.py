from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from matplotlib.style import context
from .models import LikePost, Profile, Post, Followers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username =  request.user.username)
    user_profile = user_object.profile_set.get(user = user_object)
    posts =  Post.objects.order_by('-created_at')
    users = Profile.objects.all()
    return render(request, 'index.html', {'user_profile':user_profile, 'posts' : posts, 'users': users})


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
                ------------------------------------------------------------------
                Why prefer User.objects.create_user over User.objects.create ?
                ------------------------------------------------------------------
                The most significant difference is that if you supply a password to the .create() method, 
                it will be set verbatim on the user, 
                and will not be usable to authenticate the user.
                Instead, the create_user() method hashes the password argument
                refer source: 
                https://github.com/django/django/blob/main/django/contrib/auth/models.py#L145

                ==================================================================
                '''
                user.save()
                while not Profile.objects.get(user=user):
                    continue #loop until profile instance isn't saved
                login(request, authenticate(username=username,password=password))
                return redirect('settings')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')     
    else:
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

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        image = None
        bio = request.POST['bio']
        location = request.POST['location']
        
        if request.FILES.get('image')== None:
            image= user_profile.profileimg
        else:
            image = request.FILES.get('image')
        
        user_profile.profileimg =  image
        user_profile.bio = bio
        user_profile.location = location 

        user_profile.save()

        return redirect('settings')
    return render(request, 'setting.html' , context={
        'user_profile':user_profile,
    })

@login_required(login_url="signin")
def upload(request):
    if request.method == 'POST':
        user =  Profile.objects.get(user=request.user)
        image = None
        caption = request.POST['caption']
        if request.FILES.get('image_upload') == None:
            return redirect('index')
        else:
            image = request.FILES.get('image_upload')
        post =  Post.objects.create(user=user, image=image, caption=caption)
        post.save()
        return redirect('index')
    else:
        return redirect('index')

@login_required(login_url='signin')
def like_post(request, post_id):
    like_user = Profile.objects.get(user = request.user)
    post_id = Post.objects.get(id=post_id)
    try:
        #If post is not already liked
        like_object =  LikePost.objects.create(post_object=post_id, like_usr= like_user)
        like_object.save()
    except IntegrityError:
        #If post is already liked
        like_object = LikePost.objects.get(post_object=post_id, like_usr= like_user)
        like_object.delete()
        
    return redirect('index')

def profile(request, pk):
    user = Profile.objects.get(id_user=pk)
    posts = user.post_set.all()
    logged_in_user = (str(request.user) == str(user))
    follow_status = None
    if not logged_in_user:
        if Followers.objects.filter(user=request.user, follow_usr=user).exists():
            follow_status=True
        
    return render(request, 'profile.html', context= {'user' : user, 'logged_in_user': logged_in_user , 'posts':posts, 'follow_status':follow_status})
    
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

@login_required(login_url='/')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/')
def wander(request):
    return render(request, 'wander.html')

@login_required(login_url='/')
def profile(request):
    userProfile = Profile.objects.get(user=request.user)
    data = {
        'userProfile': userProfile,
    }
    print(userProfile.user.username)
    return render(request, 'profile.html', data)

def landing(request):
    return render(request, 'landing.html')

def signupUser(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirmPassword = request.POST.get('confirmPassword')
    try:
        if password == confirmPassword:
            user = User.objects.create_user(username, email, password)
            user.save()
            Profile.objects.create(user=user)
            print('created')
            login(request, user)
            return redirect('/home/')
        else:
            print('Passwords dont match')
            return render(request, 'landing.html',{'passwordError':True})
    except Exception as e:
        try:
            user = User.objects.get(username=username)
            if user:
                print("User Exists")
                return render(request, 'landing.html',{'usernameError':True})
        except:
            try:
                user = User.objects.get(email=email)
                if user:
                    print("Email Exists")
                    return render(request, 'landing.html',{'emailError':True})
            except:
                print("Error Creating")
                return render(request, 'landing.html',{'createError':True})

def loginUser(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    print(f"Username: {user}")
    if user is not None:
        login(request, user)
        print('logged in')
        return redirect('/home/')
    else:
        print('No User')
        return render(request, 'landing.html',{'noUser':True})

def logoutUser(request):
    logout(request)
    print('logged out')
    return redirect('/')
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

@login_required(login_url='/')
def home(request):
    userProfile = Profile.objects.get(user=request.user)
    posts = Post.objects.all().order_by('-timestamp')

    left = posts[0::2]
    right = posts[1::2]

    data = {
        'userProfile': userProfile,
        'left': left,
        'right': right,
    }
    return render(request, 'home.html', data)

@login_required(login_url='/')
def wander(request):
    categories = Category.objects.all().order_by('name')
    left = categories[0::2]
    right = categories[1::2]
    data = {
        'left':left,
        'right':right
    }
    return render(request, 'wander.html', data)

@login_required(login_url='/')
def profile(request):
    userProfile = Profile.objects.get(user=request.user)
    posts = Post.objects.all().filter(creator=userProfile).order_by('-timestamp')

    left = posts[0::2]
    right = posts[1::2]

    data = {
        'userProfile': userProfile,
        'left': left,
        'right': right,
    }

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

def createPage(request):
    categories = Category.objects.all().order_by('name')
    for category in categories:
        category.sections = category.sections.replace(', ', ',').split(',')
    left = categories[0::2]
    right = categories[1::2]
    data = {
        'left':left,
        'right':right
    }
    return render(request, 'createPage.html', data)

def createCategory(request):
    category = request.POST.get('category')
    caption = request.POST.get('caption')
    description = request.POST.get('description')
    categoryPost = Category.objects.get(name=category)
    data = {
        'sections':categoryPost.sections.replace(', ', ',').split(','),
        'nextBool':True,
        'categoryChose':category,
        'caption':caption,
        'description':description,
    }
    return render(request, 'createPage.html', data)

def createPost(request, category=None):
    userProfile = Profile.objects.get(user=request.user)
    caption = request.POST.get('caption')
    description = request.POST.get('description')
    categoryPost = Category.objects.get(slug=category)
    sections = categoryPost.sections.replace(', ', ',').split(',')

    answers = []
    for section in sections:
        answers.append(request.POST.get(f'{section}'))

    name = answers[0]

    try:
        post = Post.objects.create(item_name=name,creator=userProfile,caption=caption,description=description,category=categoryPost,sections=json.dumps(sections),answers=json.dumps(answers)) #! need image, rate
        rate = len(Post.objects.all().filter(creator=userProfile))
        print(rate)
        userProfile.rates = rate
        userProfile.save()
        return redirect('/home/')
    
    except Exception as e:
        print(e)

        data = {
            'sections':categoryPost.sections.replace(', ', ',').split(','),
            'nextBool':True,
            'categoryChose':category,
            'caption':caption,
            'description':description,
        }
        return render(request, 'createPage.html', data)

@login_required(login_url='/')
def showCategory(request, category=None):
    print("Category:", category)
    categoryPost = Category.objects.get(slug=category)
    posts = Post.objects.all().filter(category=categoryPost).order_by('-timestamp')

    left = posts[0::2]
    right = posts[1::2]

    data = {
        'left':left,
        'right':right,
        'categoryBool':True,
    }
    return render(request, 'wander.html', data)
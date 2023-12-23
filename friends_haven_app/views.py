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

    idols = json.loads(userProfile.idols)
    if idols == 0:
        idols = []
    posts = Post.objects.all().filter(creator__user__username__in=idols).order_by('-timestamp')

    left = posts[0::2]
    right = posts[1::2]

    data = {
        'userProfile': userProfile,
        'left': left,
        'right': right,
        'accessProfile': userProfile
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
    profileView = True
    userProfile = Profile.objects.get(user=request.user)
    posts = Post.objects.all().filter(creator=userProfile).order_by('-timestamp')

    left = posts[0::2]
    right = posts[1::2]

    data = {
        'userProfile': userProfile,
        'left': left,
        'right': right,
        'profileView': profileView,
        'accessProfile': userProfile,
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

@login_required(login_url='/')
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

@login_required(login_url='/')
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

@login_required(login_url='/')
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
        userProfile.rates = rate
        userProfile.save()
        return redirect('/profile/')
    
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
    userProfile = Profile.objects.get(user=request.user)
    categoryPost = Category.objects.get(slug=category)
    posts = Post.objects.all().filter(category=categoryPost).order_by('-timestamp')

    left = posts[0::2]
    right = posts[1::2]

    data = {
        'left':left,
        'right':right,
        'categoryBool':True,
        'accessProfile': userProfile,
    }
    return render(request, 'wander.html', data)

@login_required(login_url='/')
def account(request, creator=None):
    userProfile = Profile.objects.get(user=request.user)
    if creator != request.user.username:
        user = User.objects.get(username=creator)
        anonymous = True
    else:
        user = request.user
        anonymous = False
    userProfile = Profile.objects.get(user=user)
    posts = Post.objects.all().filter(creator=userProfile).order_by('-timestamp')

    left = posts[0::2]
    right = posts[1::2]

    accessProfile = Profile.objects.get(user=request.user)
    accessProfileIdols = json.loads(accessProfile.idols)

    if accessProfileIdols == 0:
        accessProfileIdols = []

    data = {
        'userProfile': userProfile,
        'left': left,
        'right': right,
        'anonymous': anonymous,
        'accessProfileIdols': accessProfileIdols,
        'accessProfile': userProfile,
    }

    return render(request, 'profile.html', data)

@login_required(login_url='/')
def follow(request, username):
    fan = Profile.objects.get(user=request.user)
    idolUser = User.objects.get(username=username)
    idol = Profile.objects.get(user=idolUser)
    try:
        idols = json.loads(fan.idols)
        if idols == 0:
            idols = [str(username)]
        else:
            idols = list(idols)
            idols.append(str(username))
        fan.idols = json.dumps(idols)
        fan.idolNum = len(idols)
        fan.save()

        fans = json.loads(idol.fans)
        if fans == 0:
            fans = [str(fan.user.username)]
        else:
            fans = list(fans)
            fans.append(str(fan.user.username))
        idol.fans = json.dumps(fans)
        idol.fanNum = len(fans)
        idol.save()
    
    except Exception as e:
        print(e)

    return redirect(f'/account/{username}')

@login_required(login_url='/')
def unfollow(request, username):
    fan = Profile.objects.get(user=request.user)
    idolUser = User.objects.get(username=username)
    idol = Profile.objects.get(user=idolUser)

    idols = list(json.loads(fan.idols))
    idols.remove(str(username))
    fan.idols = json.dumps(idols)
    fan.idolNum = len(idols)
    fan.save()

    fans = list(json.loads(idol.fans))
    fans.remove(str(fan.user.username))
    idol.fans = json.dumps(fans)
    idol.fanNum = len(fans)
    idol.save()

    return redirect(f'/account/{username}')

def showIdols(request, account=None):
    if account:
        idolUser = User.objects.get(username=account)
        anonymous = True
    else:
        idolUser = request.user
        anonymous = False
    
    user = Profile.objects.get(user=idolUser)
    idols = json.loads(user.idols)
    if idols == 0:
        idols = []

    profiles = Profile.objects.all().filter(user__username__in=idols).order_by('user')

    data = {
        'anonymous':anonymous,
        'profiles':profiles,
        'account':account,
        'page':'Idols',
    }
    return render(request, 'showAccountInfo.html', data)

def showFans(request, account=None):
    if account:
        fanUser = User.objects.get(username=account)
        anonymous = True
    else:
        fanUser = request.user
        anonymous = False

    user = Profile.objects.get(user=fanUser)
    fans = json.loads(user.fans)
    if fans == 0:
        fans = []

    profiles = Profile.objects.all().filter(user__username__in=fans).order_by('user')

    data = {
        'anonymous':anonymous,
        'profiles':profiles,
        'account':account,
        'page':'Fans',
    }
    return render(request, 'showAccountInfo.html', data)

def deletePost(request, postId):
    userProfile = Profile.objects.get(user=request.user)
    post = Post.objects.get(id=postId)
    post.delete()
    rate = len(Post.objects.all().filter(creator=userProfile))
    userProfile.rates = rate
    userProfile.save()
    return redirect('/profile/')

def editPost(request, postId):
    post = Post.objects.get(id=postId)
    data = {
        'post':post,
        'edit':True
    }
    return render(request, 'editPost.html', data)

def saveEdit(request, postId):
    post = Post.objects.get(id=postId)
    start_extracting = False
    answers = []
    for key, value in request.POST.items():
        if key == 'caption':
            post.caption = value
            start_extracting = True
            continue
        elif key == 'description':
            post.description = value
            break

        if start_extracting:
            answers.append(value)

    name = answers[0]
    post.item_name = name
    post.answers = json.dumps(answers)
    post.save()

    return redirect('/profile/')

def unlikePost(request, postId):
    post = Post.objects.get(id=postId)
    likedBy = list(json.loads(post.likedBy))
    likedBy.remove(str(request.user.username))
    post.likedBy = json.dumps(likedBy)
    post.likes = len(likedBy)
    post.save()

    return redirect('/home/')

def likePost(request, postId):
    post = Post.objects.get(id=postId)
    likedBy = json.loads(post.likedBy)
    if likedBy == 0:
        likedBy = [str(request.user.username)]
    else:
        likedBy = list(likedBy)
        likedBy.append(str(request.user.username))
    post.likedBy = json.dumps(likedBy)
    post.likes = len(likedBy)
    post.save()
    
    return redirect('/home/')
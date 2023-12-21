from django.shortcuts import render, redirect
from .models import *

# Create your views here.
# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

def home(request):
    return render(request, 'home.html')

def wander(request):
    return render(request, 'wander.html')

def profile(request):
    return render(request, 'profile.html')
from django.shortcuts import render, redirect
from .models import *

# Create your views here.
# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

def index(request):
    return render(request, 'home.html')
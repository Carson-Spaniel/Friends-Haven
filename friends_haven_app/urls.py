from django.urls import path
from . import views

urlpatterns = [
    #----------------Pages----------------
    path('',views.landing, name='landing'),
    path('home/',views.home, name='home'),
    path('wander/',views.wander, name='wander'),
    path('profile/',views.profile, name='profile'),
]

from django.urls import path
from . import views

urlpatterns = [
    #----------------Pages----------------
    path('',views.home, name='home'),
    path('home/',views.home, name='home'),
    path('wander/',views.wander, name='wander'),
    path('profile/',views.profile, name='profile'),
]

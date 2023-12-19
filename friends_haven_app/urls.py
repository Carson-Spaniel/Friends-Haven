from django.urls import path
from . import views

urlpatterns = [
    #----------------Pages----------------
    path('',views.index, name='home'),
    path('home/',views.index, name='home'),
]

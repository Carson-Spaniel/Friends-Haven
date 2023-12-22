from django.urls import path
from . import views

urlpatterns = [
    #----------------Pages----------------
    path('',views.landing, name='landing'),
    path('home/',views.home, name='home'),
    path('wander/',views.wander, name='wander'),
    path('wander/<slug:category>/',views.showCategory, name='showCategory'),
    path('profile/',views.profile, name='profile'),
    path('signup/',views.signupUser, name='signup'),
    path('login/',views.loginUser, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('create/',views.createPage, name='createPage'),
    path('create/next/',views.createCategory, name='createCategory'),
    path('create/post/<str:category>',views.createPost, name='createPost'),
]

from django.urls import path
from . import views

urlpatterns = [
    #----------------Pages----------------
    path('',views.landing, name='landing'),
    path('home/',views.home, name='home'),
    path('wander/',views.wander, name='wander'),
    path('wander/<slug:category>/',views.showCategory, name='showCategory'),
    path('profile/',views.profile, name='profile'),
    path('profile/idols',views.showIdols, name='profile'),
    path('profile/fans',views.showFans, name='profile'),
    path('signup/',views.signupUser, name='signup'),
    path('login/',views.loginUser, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('create/',views.createPage, name='createPage'),
    path('create/next/',views.createCategory, name='createCategory'),
    path('create/post/<str:category>',views.createPost, name='createPost'),
    path('account/<slug:creator>/',views.account, name='account'),
    path('account/<slug:account>/idols',views.showIdols, name='account'),
    path('account/<slug:account>/fans',views.showFans, name='account'),
    path('follow/<slug:username>/',views.follow, name='follow'),
    path('unfollow/<slug:username>/',views.unfollow, name='unfollow'),
    path('delete/<int:postId>/',views.deletePost, name='deletePost'),
    path('edit/<int:postId>/',views.editPost, name='editPost'),
    path('save/<int:postId>/',views.saveEdit, name='saveEdit'),
    path('like/<int:postId>/',views.likePost, name='likePost'),
    path('unlike/<int:postId>/',views.unlikePost, name='unlikePost'),
    path('search/',views.search, name='search'),
]

from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.signout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('like_post/<str:post_id>', views.like_post, name='like_post'),
    path('profile/<str:pk>', views.profile, name='profile')

]
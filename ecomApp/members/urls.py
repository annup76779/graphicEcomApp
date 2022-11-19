from django.urls import path

from . import views

urlpatterns = [
    path('login_user', views.login_user,name='login_user'),
    path('register', views.registerTemplate, name = 'register'),
    path('postRegistration/', views.postUserRegistrationHere, name = 'postRegistration'),
    path('profile', views.profile_page, name = 'profile'),
]
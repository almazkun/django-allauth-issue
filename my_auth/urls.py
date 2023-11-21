from allauth.account import views
from django.urls import path
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path("", home, name="home"),
    path("login/", views.LoginView.as_view(), name="account_login"),
    path("logout/", views.LogoutView.as_view(), name="account_logout"),
    path("signup/", views.SignupView.as_view(), name="account_signup"),
]

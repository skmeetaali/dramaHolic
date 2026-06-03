from django.shortcuts import render
from django.urls import path
from .forms import CustomUserCreationForm, CustomUserChangeForm

urlpatterns = [
    path("signup/", CustomUserCreationForm , name="signup"),
]

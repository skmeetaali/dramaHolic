from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("valid form")
            form.save()
            return redirect("login")
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
        
    return render(request, "registration/signup.html", {"form":form})
from django.shortcuts import render, redirect
from . forms import SignupForm
from . models import Profile
from django.contrib.auth import login, logout, authenticate
# Create your views here.


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

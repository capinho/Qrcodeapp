from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def Register(request):
    if request.user.is_authenticated:
        return redirect('qrgen:dashboard')
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pswrd')
        uname = request.POST.get('email')
        if User.objects.filter(username=uname).first():
            messages.error(
                request, 'Email address already exists, register a new email address')
        else:
            new_user = User.objects.create_user(
                username=uname, email=email, password=password)
            new_user.first_name = fname
            new_user.last_name = lname
            new_user.save()
            
            # Login the new user
            login(request, new_user)
            
            # Display success message
            messages.success(request, 'Welcome to the dashboard')
            
            return redirect('qrgen:dashboard')

    return render(request, 'accounts/register.html', {})


def Login(request):
    if request.user.is_authenticated:
        return redirect('qrgen:dashboard')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pswrd')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('qrgen:dashboard'))
        else:
            messages.success(
                request, 'Email Address and Password do not exist')

    return render(request, 'accounts/login.html', {})


def logoutuser(request):
    logout(request)
    return redirect('home:home-page')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    user = request.user

    context = {
        'user': user
    }

    return render(request, 'admin/dashboard.html', context)

@login_required
def logout_user(request):
    logout(request)
    return redirect('login') 

def login(request):
    if(request.user.is_authenticated):
        return redirect('admin-dashboard')

    error_message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('admin-dashboard') 
            else:
                error_message = 'Invalid username or password.'
    else:
        form = LoginForm() 

    return render(request, 'login.html', {'form': form, 'error_message': error_message})
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


def login(request):
    context = {'debug_message': request.user}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('polls:index')
        else:
            context['error_message'] = 'Sorry, your email and password did not match'
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('home')

def signup(request):
    return render(request, 'accounts/signup.html')

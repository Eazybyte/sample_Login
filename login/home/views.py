from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth.models import User, auth
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if 'username' in request.session:
        return redirect(home)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                messages.info(request, 'Login details Incorrect')
                return redirect('signin')
            else:
                request.session['username'] = username
                return render(request, 'home.html')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if 'username' in request.session:
        return render(request, 'home.html')
    return redirect('signin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('signin')
          
def signup(request):
    if request.method == 'POST':
        full_name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['re-password']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'user name taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Account exists')
                return redirect('signin')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=full_name)
                user.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'register.html')

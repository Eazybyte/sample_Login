from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth.models import User, auth
# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if 'adminuser' in request.session:
        return redirect(home)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                if user.is_superuser:
                    request.session['adminuser'] = username
                    return redirect(home)

                else:
                    messages.info(request, 'Login details Incorrect')
                    return redirect('signin')

            else:
                messages.info(request, 'Invalid credentials')
                return redirect('signin')
        else:
            return render(request, 'admin_login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if 'adminuser' in request.session:
        context = {'usr': User.objects.all()}
        return render(request, 'admin_home.html', context)
    return redirect('signin')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signout(request):
    if 'adminuser' in request.session:
        del request.session['adminuser']
        return redirect(signin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adduser(request):
    if 'adminuser' in request.session:
        if request.method == 'POST':
            full_name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            if User.objects.filter(username=username).exists():
                messages.info(request, 'user name taken')
                return redirect(home)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Account exists')
                return redirect(home)
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email, first_name=full_name)
                user.save()
                return redirect(home)
        else:
            return render(request, 'admin_adduser.html')
    else:
        return redirect(signin)

def delete_user(request, id):
    if 'adminuser' in request.session:
        Deluser = User.objects.get(id=id)
        Deluser.delete()
        return redirect(home)
        

def update(request, id):
    if 'adminuser' in request.session:
        if request.method == 'POST':
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']

            updateuser = User.objects.get(id=id)
            updateuser.first_name = name
            updateuser.username = username
            updateuser.email = email
            updateuser.save()
            return redirect(home)
        else:
            context = {'user': User.objects.get(id=id)}
            return render(request, "admin_edituser.html", context)
    else:
        return redirect(signin)


def search(request):
    if 'adminuser' in request.session:
        usrname = request.GET['uname']
        searchuser = User.objects.filter(username__icontains=usrname).values()
        return render(request, "admin_search.html", {'user': searchuser})
    else:
        return redirect(signin)

    
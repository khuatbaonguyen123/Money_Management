# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CustomUserCreationForm()
        if request.method=="POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user_name = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user_name)
                return redirect('login')
            else:
                # You can also display errors to the user using messages or directly passing it to the context
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                for error in form.non_field_errors():
                    messages.error(request, error)
        else:
            form = CustomUserCreationForm()
        context = {'form':form}
        return  render(request, "users/register.html", context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else: 
        if request.method=="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect.')

        context = {}
        return render(request, 'users/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')

login_required(login_url='login')
def homePage(request):
    context ={}
    return render(request, 'users/home.html', context)

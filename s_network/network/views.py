from django.shortcuts import render, redirect
from .forms import PageForm, UserRegisterForm, UserLoginForm
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import login, logout


def index(request):
    return render(request, template_name='network/index.html')


class CreatePage(CreateView):
    form_class = PageForm
    template_name = 'network/add_page.html'


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'network/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'network/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')





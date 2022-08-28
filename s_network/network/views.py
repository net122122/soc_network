from django.shortcuts import render, redirect
from .forms import PageForm, UserRegisterForm, UserLoginForm
from django.views.generic import CreateView, DetailView, ListView
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import Page
from django.core.paginator import Paginator


def index(request):
    return render(request, template_name='network/index.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = PageForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_user.refresh_from_db()
            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            login(request, new_user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
            # new_profile = PageForm()
            # return render(request, 'network/register.html', {
            #     'user_form': user_form,
            #     'new_profile': new_profile
            # })
    else:
        user_form = UserRegisterForm()
        new_profile = PageForm()
        return render(request, 'network/register.html', {
            'user_form': user_form,
            'new_profile': new_profile
            })


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


class ViewPage(DetailView):
    model = Page
    context_object_name = 'page_item'


class GetUsers(ListView):
    model = Page
    template_name = 'network/get_users.html'
    context_object_name = 'get_users'
    paginate_by = 5


class MyPage(ListView):
    model = Page
    template_name = 'network/my_page.html'
    context_object_name = 'my_page'

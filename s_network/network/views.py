from django.shortcuts import render, redirect, get_object_or_404
from .forms import PageForm, UserRegisterForm, UserLoginForm, PageEditForm
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Page, Relationship
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    page = Page.objects.get(user=request.user)
    context = {
        'page': page
    }
    return render(request, 'network/index.html', context)


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
            return redirect('my_page')
        else:
            messages.error(request, 'Ошибка регистрации')
            new_profile = PageForm()
            return render(request, 'network/register.html', {
                'user_form': user_form,
                'new_profile': new_profile
            })
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
            return redirect('my_page')
    else:
        form = UserLoginForm()
    return render(request, 'network/login.html', {"form": form})


@login_required
def edit(request):
    if request.method == 'POST':
        page_form = PageEditForm(instance=request.user.page, data=request.POST, files=request.FILES)
        if page_form.is_valid():
            page_form.save()
            return redirect('my_page')
    else:
        page_form = PageEditForm(instance=request.user.page)
        return render(request,
                      'network/edit.html', {
                       'page_form': page_form})


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


@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, created, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()


class MyFriends(ListView):
    model = Page
    template_name = 'network/my_friends.html'
    context_object_name = 'my_friends'



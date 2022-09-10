from django.shortcuts import render, redirect, get_object_or_404
from .forms import PageForm, UserRegisterForm, UserLoginForm, PageEditForm
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Page, Relationship
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.db.models import Q

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
def change_friend(sender, created, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()


@receiver(pre_delete, sender=Relationship)
def pre_delete_from_friends(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()


@login_required
def remove_friend(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('page_pk')
        sender = Page.objects.get(user=user)
        receiver = Page.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('get_users')


@login_required
def add_friend(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('page_pk')
        sender = Page.objects.get(user=user)
        receiver = Page.objects.get(pk=pk)

        rel = Relationship.objects.create(
            sender=sender, receiver=receiver, status='accepted'
        )
        rel.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('get_users')


@login_required
def like_page(request):
    user = request.user
    if request.method == 'POST':
        page_id = request.POST.get('page_pk')
        page_obj = Page.objects.get(id=page_id)

        if user in page_obj.liked.all():
            page_obj.liked.remove(user)
        else:
            page_obj.liked.add(user)

        # like = Like.objects.get_or_create(user=user, page_id=page_id)
        #
        # if like.value == 'Лайк':
        #     like.value = 'Убрать лайк'
        # else:
        #     like.value = 'Лайк'
        # like.sasve()
    return redirect(request.META.get('HTTP_REFERER'))


class MyFriends(ListView):
    model = Page
    template_name = 'network/my_friends.html'
    context_object_name = 'my_friends'


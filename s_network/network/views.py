from django.shortcuts import render
from .forms import PageForm
from django.views.generic import CreateView


def index(request):
    return render(request, template_name='network/index.html')


class CreatePage(CreateView):
    form_class = PageForm
    template_name = 'network/add_page.html'





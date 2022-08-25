from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('network/add-page/', CreatePage.as_view(), name='add_page')
]
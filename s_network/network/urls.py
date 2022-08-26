from django.urls import path

from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', index, name='home'),
    path('network/add-page/', CreatePage.as_view(), name='add_page'),
    path('network/get-users/', get_users, name='get_users')
]
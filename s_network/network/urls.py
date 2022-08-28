from django.urls import path

from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', index, name='home'),
    path('network/get-users/', GetUsers.as_view(), name='get_users'),
    path('network/my-page/', MyPage.as_view(), name='my_page'),
    path('network/<int:pk>/', ViewPage.as_view(), name='view_page'),
]


from django.urls import path
from . import views


from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    # path('', index, name='home'),
    path('', index, name='home'),
    path('network/get-users/', GetUsers.as_view(), name='get_users'),
    path('network/my-page/', MyPage.as_view(), name='my_page'),
    path('network/my-friends/', MyFriends.as_view(), name='my_friends'),
    path('network/<int:pk>/', ViewPage.as_view(), name='view_page'),
    path('network/edit/', edit, name='edit'),
    path('network/remove-friend/', remove_friend, name='remove_friend'),
    path('network/add-friend/', add_friend, name='add_friend'),
    path('network/like-page/', like_page, name='like_page'),
]


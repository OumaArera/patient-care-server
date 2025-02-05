from django.urls import path # type: ignore
from users.views import *

urlpatterns=[
    path(
        'users',
        UserView.as_view(), 
        name='users'
    ),
    path(
        'users/<int:userId>',
        UserQueryByIDView.as_view(), 
        name='user-details'
    ),

]
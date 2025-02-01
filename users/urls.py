from django.urls import path # type: ignore
from users.views import *

urlpatterns=[
    path(
        'create-users',
        UserView.as_view(), 
        name='create-users'
    ),
    path(
        'create-users/<int:userId>',
        UserQueryByIDView.as_view(), 
        name='create-user-details'
    ),

]
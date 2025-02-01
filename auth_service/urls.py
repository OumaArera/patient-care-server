from django.urls import path # type: ignore

from auth_service.views.change_password_view import ChangePasswordView
from auth_service.views.login_view import LoginView
from auth_service.views.reset_password import ResetPasswordView # type: ignore

urlpatterns=[
    
    path(
        'login',
        LoginView.as_view(), 
        name='login'
    ),
    path(
        'change-password',
        ChangePasswordView.as_view(), 
        name='change-password'
    ),
    path(
        'reset-password',
        ResetPasswordView.as_view(), 
        name='reset-password'
    ),

]
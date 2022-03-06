from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.urls import path
from django.urls.base import reverse_lazy

from . import views

#from django_otp.forms import OTPAuthenticationForm


app_name = 'users'



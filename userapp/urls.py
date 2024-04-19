from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.signout, name='logout'),
    path('reset_password/<uidb64>/<token>', views.reset_password, name='reset_password'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('activate_account/<uidb64>/<token>', views.activate_account, name='activate_account'),
]

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='main_page'),
    path('login', views.login_acc, name='login'),
    path('registration', views.reg, name='reg'),
    path('complete', views.complete, name='complete'),
    path('profile', views.profile, name='profile'),
    path('change', views.change_pswrd, name='change_pswrd')
]

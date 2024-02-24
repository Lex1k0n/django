from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('mail', views.add, name='add_mail'),
    path('bp', views.bp, name='add_bp'),
]

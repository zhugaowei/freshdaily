from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('login_handle/',views.login_handle),
    path('info/', views.info),
    path('order/', views.order),
    path('site/', views.site),
    path('register_handle/', views.register_handle),
    path('logout/',views.logout),
]
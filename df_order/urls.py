from django.contrib import admin
from django.urls import path
# from django.conf.urls import include
from .import views

urlpatterns = [

    path('',views.order),
    path('order_handle/',views.order__handle),
]
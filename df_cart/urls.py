from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [

    path('',views.cart),
    path('<int:gid>/<int:count>/',views.add),
    path('edit/<int:cart_id>/<int:count>/',views.edit),
    path('delete/<int:id>/',views.delete),
]
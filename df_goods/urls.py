from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views
urlpatterns = [
    path('list/<int:tid>/<int:pindex>/<int:sort>/',views.list),
    path('index/',views.index),
    path('detail/<int:id>/',views.detail),
]

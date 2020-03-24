from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('algorithm/<int:current>/', views.algorithm, name='algorithm'),
    path('editor/', views.editor, name='editor'),
    path('logout/', views.logout, name='logout')
    ]
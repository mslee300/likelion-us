from django.urls import path

from . import views

app_name = 'likelion'

urlpatterns = [
    path('', views.index, name='index'),
    path('my-profile/', views.my_profile, name='my-profile'),
]

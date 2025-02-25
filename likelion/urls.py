from django.urls import path

from . import views

app_name = 'likelion'

urlpatterns = [
    path('', views.index, name='index'),
    path('my-list/', views.my_list, name='my-list'),
    path('my-profile/', views.my_profile, name='my-profile'),
    path('search/', views.search, name='search'),
    path('person/', views.person, name='person'),
    path('company/', views.company, name='company')
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='button'),
    path('vk_data/', views.get_vk_data, name='vk_data')
    path('get_user_info/', views.get_vk_code, name='user_info')
]


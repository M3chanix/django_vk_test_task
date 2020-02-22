from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='button'),
    path('get_vk_data/', views.get_vk_data, name='get_vk_data'),
    path('check_auth/', views.check_auth, name='check_auth'),
    path('login/', views.login, name='login'),
    path('authorize/', views.authorize, name='authorize')
]


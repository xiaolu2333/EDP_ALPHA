from django.urls import path

from edp_user import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='register')
]
from django.urls import path

from edp_user import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    path('api/v1/', views.user_list, name="user-list"),
    path('api/v1/<int:pk>', views.user_detail, name="user-detail"),
]

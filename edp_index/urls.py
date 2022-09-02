from django.urls import path

from edp_index import views

urlpatterns = [
    path('', views.index, name='index')
]

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('', views.home, name='home'),
    path('view/<str:link>/', views.view_file, name='view_file'),

]
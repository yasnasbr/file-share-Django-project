from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload),
    path('s/<str:link>/', views.download),
]
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.Upload.as_view(), name='upload'),
    path('', views.AllFiles.as_view(), name='all_files'),
    path('view/<str:link>/', views.ViewUploadedFile.as_view(), name='view_file'),
]
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('upload/', views.Upload.as_view(), name='upload'),
    path('', views.AllFiles.as_view(), name='all_files'),
    path('view/<str:link>/', views.ViewUploadedFile.as_view(), name='view_file'),
]
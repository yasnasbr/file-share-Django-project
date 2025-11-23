import django_filters
from .models import UploadedFile

class FileFilter(django_filters.FilterSet):
    class Meta:
        model = UploadedFile
        fields = ['title','is_public','expire_date']
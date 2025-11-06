
from rest_framework import serializers

from .models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(read_only=True)
    class Meta:
        model = UploadedFile
        fields = ['title','file','share_link', 'views','expire_date', 'is_public','upload_date']


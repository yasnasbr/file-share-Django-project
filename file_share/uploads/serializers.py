
from rest_framework import serializers
from django.conf import settings
from .models import UploadedFile
from django.utils import timezone


class UploadedFileSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    qr = serializers.SerializerMethodField()
    time_left = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        fields = ['title', 'link', 'qr', 'downloads', 'time_left']


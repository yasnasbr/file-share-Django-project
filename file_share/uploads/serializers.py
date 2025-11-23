from rest_framework import serializers
from .models import UploadedFile

class UploadedFileSerializer(serializers.ModelSerializer):
    file= serializers.FileField(read_only=True)
    class Meta:
        model = UploadedFile
        fields = ['title','file','share_link','expire_date', 'is_public','upload_date']

class InputFileSerializer(serializers.ModelSerializer):
    expire_days = serializers.IntegerField(required=False, min_value=1, max_value=30,default=3)
    title = serializers.CharField(required=True, allow_blank=False)
    file= serializers.FileField(required=True)

    class Meta:
        model = UploadedFile
        fields = ['title','file','expire_days','is_public','password']

    def validate(self, attrs):

        is_public = attrs.get('is_public', True)
        password = attrs.get('password')
        if is_public is False and not password:
            raise serializers.ValidationError({"password": "password is required for private file"})
        if is_public:
            attrs['password'] = ''
        return attrs

class ErrorResponseSerializer(serializers.Serializer):
    ok = serializers.BooleanField(default=False)
    error = serializers.CharField()




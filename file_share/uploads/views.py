from django.http import Http404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .file_service import upload_file, verify_password
from .filters import FileFilter
from .models import UploadedFile
from .serializers import UploadedFileSerializer, InputFileSerializer, ErrorResponseSerializer

"""this cbv handles upload requests ,
    saves files info to database ,
    schedules automatic deletion using Celery ,
    returns uploaded file info as Response
"""
class Upload(GenericAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = InputFileSerializer
    @extend_schema(
        summary='Upload file',
        request=InputFileSerializer,
        responses={
            201: UploadedFileSerializer,
            400:ErrorResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = UploadedFile(file=serializer.validated_data['file'])
        uploaded_file = upload_file(uploaded_file, serializer.validated_data)
        out_serializer = UploadedFileSerializer(uploaded_file, context={'request': request})
        return Response({"ok": True, "data": out_serializer.data}, status=201)

"""this cbv handles get requests to view uploaded file's information:
    validates the share link,
    checks expiration status,
    if file is private, verifies password,
    increments view count
"""
class ViewUploadedFile(GenericAPIView):
    serializer_class = UploadedFileSerializer
    queryset = UploadedFile.objects.all()
    lookup_field = 'share_link'
    lookup_url_kwarg = 'link'
    def get(self, request, link, *args, **kwargs):
        try:
            obj = self.get_object()
        except Http404:
            return Response({"ok": False, "error": "File not found"}, status=404)
        if obj.expire_date and obj.expire_date < timezone.now():
            return Response({"ok": False, "error": "File is expired"}, status=404)

        if not obj.is_public:
            password = request.query_params.get('password')
            if not verify_password(obj, password):
                return Response({"ok": False, "error": "Incorrect password"}, status=403)

        serializer = self.get_serializer(obj, context={'request': request})
        return Response({"ok": True, "data": serializer.data}, status=200)



class AllFiles(ListAPIView):
    queryset = UploadedFile.objects.all().order_by('-upload_date')
    serializer_class = UploadedFileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class=FileFilter

    @extend_schema(
        description='View all files',
        responses={200: UploadedFileSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)




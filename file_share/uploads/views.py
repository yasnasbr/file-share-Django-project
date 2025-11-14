import uuid

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .file_service import upload_file, check_expired, verify_password
from .forms import UploadForm
from .models import UploadedFile
from .serializers import UploadedFileSerializer

"""this cbv handles upload requests ,
    saves files info to database ,
    schedules automatic deletion using Celery ,
    returns uploaded file info as Response
"""
class Upload(APIView):
    def post(self, request):
        form = UploadForm(request.data, request.FILES)
        if not form.is_valid():
            return Response(
                {"ok": False, "errors": form.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        uploaded_file = form.save(commit=False)
        if 'file' in request.FILES:
            uploaded_file.file = request.FILES['file']
        uploaded_file = upload_file(uploaded_file, form.cleaned_data)
        serializer = UploadedFileSerializer(uploaded_file, context={'request': request})

        return Response(
            {"ok": True, "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
"""this cbv handles get requests to view uploaded file's information:
    validates the share link,
    checks expiration status,
    if file is private, verifies password,
    increments view count
"""
class ViewUploadedFile(APIView):
    def get(self, request, link):
        try:
            file = get_object_or_404(UploadedFile, share_link=link)
            check_expired(file.expire_date)
        except NotFound:
            return Response({"ok": False, "error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        if not file.is_public:
            password = request.query_params.get("password")
            if not verify_password(file, password):
                return Response({"ok": False, "error": "Incorrect password"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UploadedFileSerializer(file, context={'request': request})
        return Response({"ok": True, "data": serializer.data}, status=status.HTTP_200_OK)


class AllFiles(APIView):
    def get(self):
        files = UploadedFile.objects.all().order_by('-upload_date')
        serializer = UploadedFileSerializer(files, many=True)
        return Response({"ok": True, "data": serializer.data}, status=status.HTTP_200_OK)




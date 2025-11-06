from django.utils import timezone

from .models import UploadedFile


def delete_expired_files():
    now = timezone.now()
    expired_files = UploadedFile.objects.filter(expire_date__lt=now)
    for obj in expired_files:
        if obj.file:
            obj.file.delete(save=False)
        obj.delete()

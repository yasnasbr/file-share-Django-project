import logging
from celery import shared_task
from django.utils import timezone

from .models import UploadedFile
logger = logging.getLogger(__name__)
@shared_task
def delete_expired_files():
    now = timezone.now()
    expired_files = UploadedFile.objects.filter(expire_date__lte=now)

    for f in expired_files:
        try:
            if f.file:
                f.file.delete(save=False)
            logger.info(f"Deleted expired file: {f.file.name}")
            f.delete()
        except Exception as e:
            logger.error(f"Error deleting file {f.id}: {e}")

    logger.info(f"{expired_files.count()} expired files deleted")




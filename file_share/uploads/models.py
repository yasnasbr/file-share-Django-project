import datetime
import os
import uuid
from datetime import timezone
from typing import Any

from django.db import models

from django.utils import timezone




# this function will be used when the user specifies the link's expiration time
def expire_time(days:int):
    return timezone.now() + datetime.timedelta(days=days)
#this function will be used when the user doesn't specify the link's expiration time, and the app saves it for three days by default
def default_expire_time():
    return timezone.now() + datetime.timedelta(days=3)
def upload_path(instance, filename):
    return f'uploads/{uuid.uuid4().hex}_{filename}'

class UploadedFile(models.Model):
    upload_date= models.DateTimeField(auto_now_add=True)
    expire_date= models.DateTimeField(default=default_expire_time)
    file= models.FileField(upload_to=upload_path)
    title= models.CharField(max_length=120)
    share_link = models.CharField(max_length=10, unique=True, blank=True, editable=False)
    is_public = models.BooleanField(default=True)
    password=models.CharField(max_length=128,null=True,blank=True)

    class Meta:
        ordering=['upload_date']

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)
        self.id = None

    def save(self, *args, **kwargs):
        if not self.share_link:
            self.share_link = uuid.uuid4().hex[:10]
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)



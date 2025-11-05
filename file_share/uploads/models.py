import datetime
import random
import string
import uuid
from datetime import timezone
from django.db import models

from django.utils import timezone


# Create your models here.


def expire_time():
    return timezone.now() + datetime.timedelta(days=3)
def upload_path(instance, filename):
    return f'uploads/{uuid.uuid4().hex}_{filename}'

class UploadedFile(models.Model):
    upload_date= models.DateTimeField(auto_now_add=True)
    expire_date= models.DateTimeField(default=expire_time)
    file= models.FileField(upload_to=upload_path)
    title= models.CharField(max_length=120)
    share_link = models.CharField(max_length=10, unique=True, blank=True, editable=False)
    downloads= models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)
    password=models.CharField(max_length=128,null=True,blank=True)

    class Meta:
        ordering=['upload_date']

    def save(self, *args, **kwargs):
        if not self.share_link:
            self.share_link = uuid.uuid4().hex[:10]
        super().save(*args, **kwargs)



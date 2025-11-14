import uuid
from datetime import timedelta
from django.http import Http404
from django.utils import timezone
from .models import UploadedFile


"""this function handles uploading a file by assigning a unique share link, title, 
    public status, optional password, and expiration date.
"""
def upload_file(uploaded: UploadedFile, cleaned_data: dict) -> UploadedFile:
    uploaded.share_link = uuid.uuid4().hex[:10]
    uploaded.title = cleaned_data.get('title','')
    uploaded.is_public = cleaned_data.get('is_public', True)
    uploaded.password = cleaned_data.get('password') or None
    expire_days = cleaned_data.get('expire_days')
    uploaded.expire_date = timezone.now() + timedelta(days=expire_days or 3)
    uploaded.save()
    return uploaded

def check_expired(expire_date):
    if timezone.now() > expire_date:
        raise Http404("link is expired")

def is_public(file:UploadedFile):
    return bool(file.is_public)

def verify_password(file:UploadedFile,password):
    return bool(file.password == password)














    
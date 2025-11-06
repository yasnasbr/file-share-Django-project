import os
import uuid
from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from .forms import UploadForm
from .models import UploadedFile

"""this view function gets information from form (title,expire date , public or private
,and the function creates the link and saves the file """
def upload(request):
        form = UploadForm(request.POST or None, request.FILES or None)
        if request.method== 'POST' and form.is_valid():
            uploaded= form.save(commit=False)
            uploaded.share_link = uuid.uuid4().hex[:10]
            expire_days = form.cleaned_data.get('expire_days')
            if expire_days:
                uploaded.expire_date = timezone.now()+ timedelta(days=expire_days)
            uploaded.is_public = form.cleaned_data.get('is_public', True)
            password = form.cleaned_data.get('password')
            if password:
                uploaded.password = password
            else:
                uploaded.password = None

            uploaded.save()
            return render(request,'success.html', {'link': uploaded.share_link, 'obj': uploaded})
        return render(request,'upload_form.html', {'form': form})

"""this view function is used when the users wants to visit a link ,
it checks if the link is expired or not,
and also asks the user to enter a password when the link is private"""

def view_file(request, link):
    file=get_object_or_404(UploadedFile, share_link=link)

    if timezone.now()>file.expire_date:
        file.file.delete()
        file.delete()
        raise Http404("this link is expired")

    if not file.is_public:
        if request.method == "POST":
            password = request.POST.get('password')
            if password != file.password:
                return render(request, 'password.html', {'link': link, 'error': 'Incorrect password'})
        else:
            return render(request, 'password.html', {'link': link})

    file.views += 1

    file.save()

    filename = file.file.name.lower()
    file_ext = os.path.splitext(filename)[1]

    if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        file_type = 'image'
    elif file_ext in ['.mp4', '.webm', '.ogg']:
        file_type = 'video'
    elif file_ext == '.pdf':
        file_type = 'pdf'
    else:
        file_type = 'other'

    context = {
        'obj': file,
        'file_type': file_type
    }
    return render(request, 'file.html', context)


def home(request):
    files = UploadedFile.objects.all().order_by('-upload_date')
    for f in files:
        f.is_expired = timezone.now() > f.expire_date
    return render(request, 'home.html', {'files': files})




import uuid

from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from django.utils import timezone

from .forms import UploadForm
from .models import UploadedFile



def upload(request):
        form = UploadForm(request.POST or None, request.FILES or None)

        if request.method == 'POST' and form.is_valid():
            uploaded = form.save(commit=False)
            uploaded.share_link = uuid.uuid4().hex[:10]
            uploaded.save()
            return render(request, 'success.html', {'link': uploaded.share_link, 'obj': uploaded})
        return render(request, 'upload.html', {'form': form})


def download(request, link):
    file=get_object_or_404(UploadedFile, share_link=link)

    if timezone.now()>file.expire_date:
        file.file.delete()
        file.delete()
        raise Http404("this link is expired")

    if not file.is_public:
        if request.GET.get('pwd') != file.password:
            return render(request, 'password.html', {'link': link})

    file.downloads+= 1
    file.save()
    return render(request, 'file.html', {'obj': file})


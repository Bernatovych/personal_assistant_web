from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from file_sorter.models import UploadFile
from .forms import UploadFileForm
from django.contrib import messages
from os import path
from django.conf import settings
import shutil

def sort_files(files_list, username):
    CATEGORIES = {
        'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
        'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
        'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
        'video': ('AVI', 'MP4', 'MOV', 'MKV'),
        'archives': ('ZIP', 'GZ', 'TAR')
    }
    media_path = Path(settings.MEDIA_ROOT, username)
    for file1 in files_list:
        ext = Path(file1.name).suffix[1:]
        for key, value in CATEGORIES.items():
            if ext.upper() in value:
                new_path = media_path.joinpath(key)
                break
        new_path.mkdir(parents=True, exist_ok=True)
        with open(new_path.joinpath(file1.name), 'wb+') as f:
            shutil.copyfileobj(file1, f)


@login_required
def uploadfile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('loaded_file')
        print('--- TYPE:', type(request.FILES['loaded_file']))
        if form.is_valid():
            # form = form.save(commit=False)
            # form.user = request.user
            # form.save()
            # sort_files(files)
            # messages.success(request, 'The file is saved successfully.')
            # return redirect('file_sorter')
            sort_files(files, request.user.username)
            context = {'msg' : '<span style="color: green;">File successfully uploaded</span>'}
            return render(request, "uploadfoles.html", {'form': form})
        else:
            messages.error(request, f'The following error has occured: {form.errors.as_data()}')
            return redirect('file_sorter')
    else:
        form = UploadFileForm()
    return render(request, 'uploadfoles.html', {'form': form})

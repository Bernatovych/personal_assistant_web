import shutil
from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import UploadFileForm

def determine_path(ext, username):
    uploads_path = Path(settings.UPLOADS_ROOT, username)
    cat_key, cat_val = settings.CATEGORIES.keys(), settings.CATEGORIES.values()
    append_path = ''.join(list(map(lambda key, value: key if ext.upper() in value else '', cat_key, cat_val)))
    append_path = append_path if len(append_path) else 'other'
    return uploads_path.joinpath(append_path)

def sort_files(req, files_list, username):
    for file1 in files_list:
        new_path = determine_path(Path(file1.name).suffix[1:], username)
        new_path.mkdir(parents=True, exist_ok=True)
        with open(new_path.joinpath(file1.name), 'wb+') as f:
            shutil.copyfileobj(file1, f)
    messages.success(req, message=f"files \"{', '.join([f.name for f in files_list])}\" successfully uploaded")

@login_required
def uploadfile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('loaded_file')
        if form.is_valid():
            sort_files(request, files, request.user.username)
            return render(request, "uploadfoles.html", {'form': form})
        else:
            messages.error(request, f'The following error has occured: {form.errors.as_data()}')
            return redirect('file_sorter')
    else:
        form = UploadFileForm()
    return render(request, 'uploadfoles.html', {'form': form})

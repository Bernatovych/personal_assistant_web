from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from file_sorter.models import UploadFile
from .forms import UploadFileForm
from django.contrib import messages
from os import path

@login_required
def uploadfile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('loaded_file')
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            # for f in files:
            #     file_instance = UploadFile(user_id=str(request.user.id), loaded_file=path.join(str(request.user.id), '2', str(f)))
            #     file_instance.save()
            messages.success(request, 'The file is saved successfully.')
            return redirect('file_sorter')
        else:
            messages.error(request, f'The following error has occured: {form.errors.as_data()}')
            return redirect('file_sorter')
    else:
        form = UploadFileForm()
    return render(request, 'uploadfoles.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from .forms import UploadFileForm
from django.contrib import messages


@login_required
def uploadfile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'The file is saved successfully.')
            return redirect('file_sorter')
        else:
            messages.error(request, f'The following error has occured: {form.errors.as_data()}')
            return redirect('file_sorter')
    else:
        form = UploadFileForm()
    return render(request, 'uploadfoles.html', {'form': form})

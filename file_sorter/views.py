import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView

from contact_book.views import UserAccessTestMixin
from file_sorter.filters import FileFilter
from file_sorter.forms import FileAddForm
from django.views.generic.edit import FormView, DeleteView
from file_sorter.models import File
import mimetypes


class FilesAddFormView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = FileAddForm
    template_name = 'upload_form.html'
    success_url = reverse_lazy('files_list')
    success_message = f'Files was added successfully'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        if form.is_valid():
            for f in files:
                File.objects.create(user=self.request.user, file=f)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class FilesListView(LoginRequiredMixin, ListView):
    template_name = 'files.html'
    paginate_by = 10
    model = File

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FileFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user).order_by('-created')
        files = FileFilter(self.request.GET, queryset=qs)
        return files.qs


class ImagesListView(LoginRequiredMixin, ListView):
    template_name = 'files.html'
    paginate_by = 10
    model = File

    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user).filter(category='images').order_by('-created')
        return qs


class DocumentsListView(LoginRequiredMixin, ListView):
    template_name = 'files.html'
    paginate_by = 10
    model = File

    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user).filter(category='documents').order_by('-created')
        return qs


class AudioListView(LoginRequiredMixin, ListView):
    template_name = 'files.html'
    paginate_by = 10
    model = File

    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user).filter(category='audio').order_by('-created')
        return qs


class VideoListView(LoginRequiredMixin, ListView):
    template_name = 'files.html'
    paginate_by = 10
    model = File

    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user).filter(category='video').order_by('-created')
        return qs


class ArchivesListView(LoginRequiredMixin, ListView):
    template_name = 'files.html'
    paginate_by = 10
    model = File

    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user).filter(category='archives').order_by('-created')
        return qs


class OtherListView(LoginRequiredMixin, ListView):
    template_name = 'files.html'
    paginate_by = 10
    model = File

    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user).filter(category='other').order_by('-created')
        return qs


def file_download(request, pk):
    file = get_object_or_404(File, pk=pk)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    link = str(file.file)
    file_path = BASE_DIR + '/' + link
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404


class FileDeleteView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, DeleteView):
    model = File
    template_name = 'file_delete_form.html'
    success_url = reverse_lazy('files_list')
    success_message = 'File (%(file)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if os.path.exists(str(obj.file)):
            os.remove(str(obj.file))
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(FileDeleteView, self).delete(request, *args, **kwargs)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from note_book.filters import NoteFilter
from note_book.models import Note, Tag
from django.contrib import messages


class NotePageView(LoginRequiredMixin, ListView):
    template_name = 'notes.html'
    paginate_by = 10
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NoteFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user)
        contacts = NoteFilter(self.request.GET, queryset=qs)
        return contacts.qs


class NoteAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Note
    fields = ['text']
    template_name = 'add_form.html'
    success_url = reverse_lazy('note_book')
    success_message = 'Note was created successfully'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        form.save()
        return super(NoteAddView, self).form_valid(form)


class TagAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tag
    fields = ['tag']
    template_name = 'add_form.html'
    success_url = reverse_lazy('note_book')
    success_message = 'Tag was created successfully'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.note = Note.objects.get(id=self.kwargs['pk'])
        form.save()
        return super(TagAddView, self).form_valid(form)


class NoteUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Note
    fields = ['text']
    template_name = 'update_form.html'
    success_url = reverse_lazy('note_book')
    success_message = 'Note (%(text)s) was updated successfully'


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'delete_form.html'
    success_url = reverse_lazy('note_book')
    success_message = 'Note (%(text)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(NoteDeleteView, self).delete(request, *args, **kwargs)


class TagUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tag
    fields = ['tag']
    template_name = 'update_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Email (%(tag)s) was updated successfully'


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'delete_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Contact (%(tag)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(TagDeleteView, self).delete(request, *args, **kwargs)
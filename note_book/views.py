from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from contact_book.views import UserAccessTestMixin
from note_book.filters import NoteFilter
from note_book.forms import NoteAddForm, TagAddForm
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
        qs = self.model.objects.filter(user=self.request.user).order_by('text')
        contacts = NoteFilter(self.request.GET, queryset=qs)
        return contacts.qs


@login_required
def note_add(request):
    form = NoteAddForm(request.POST)
    form_tag = TagAddForm(request.POST)
    if request.method == 'POST':
        if form.is_valid() and form_tag.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            tag = form_tag.cleaned_data['tag']
            if tag:
                Tag.objects.create(tag=tag, note=form, user=request.user)
            messages.success(request, 'Contact was created successfully')
            return redirect('note_book')
    else:
        form = NoteAddForm()
        form_tag = TagAddForm()
    return render(request, 'note_form.html', {'form': form, 'form_tag': form_tag})


class TagAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tag
    fields = ['tag']
    template_name = 'note_add_form.html'
    success_url = reverse_lazy('note_book')
    success_message = 'Tag was created successfully'

    def form_valid(self, form):
        obj = form.save(commit=False)
        note = Note.objects.get(id=self.kwargs['pk'])
        if note.user == self.request.user:
            obj.note = Note.objects.get(id=self.kwargs['pk'])
            obj.user = self.request.user
            form.save()
        else:
            raise PermissionDenied
        return super(TagAddView, self).form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Note
    fields = ['text']
    template_name = 'note_update_form.html'
    success_url = reverse_lazy('note_book')
    success_message = 'Note (%(text)s) was updated successfully'


class NoteDeleteView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = 'note_delete_form.html'
    success_url = reverse_lazy('note_book')
    success_message = 'Note (%(text)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(NoteDeleteView, self).delete(request, *args, **kwargs)


class TagUpdateView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Tag
    fields = ['tag']
    template_name = 'note_update_form.html'
    success_url = reverse_lazy('note_book')
    success_message = 'Tag (%(tag)s) was updated successfully'


class TagDeleteView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, DeleteView):
    model = Tag
    template_name = 'note_delete_form.html'
    success_url = reverse_lazy('note_book')
    success_message = 'Tag (%(tag)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(TagDeleteView, self).delete(request, *args, **kwargs)
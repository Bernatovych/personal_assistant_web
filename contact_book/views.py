from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, ListView, DeleteView, UpdateView
from contact_book.filters import ContactFilter
from contact_book.forms import ContactAddForm
from contact_book.models import Contact, Phone, Address, Email
from django.contrib import messages


class HomePageView(LoginRequiredMixin, ListView):
    template_name = 'home.html'
    paginate_by = 10
    model = Contact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ContactFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user)
        contacts = ContactFilter(self.request.GET, queryset=qs)
        return contacts.qs


class ContactAddMixin(object):

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.contact = Contact.objects.get(id=self.kwargs['pk'])
        form.save()
        return super(ContactAddMixin, self).form_valid(form)


class ContactAddView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    model = Contact
    form_class = ContactAddForm
    template_name = 'add_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Contact was created successfully'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        form.save()
        return super(ContactAddView, self).form_valid(form)


class PhoneAddView(ContactAddMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Phone
    fields = ['phone_number']
    template_name = 'add_form.html'
    success_url = reverse_lazy('home')
    success_message = f'{model.__name__} was created successfully'


class AddressAddView(ContactAddMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Address
    fields = ['address']
    template_name = 'add_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Address was created successfully'


class EmailAddView(ContactAddMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Email
    fields = ['email']
    template_name = 'add_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Email was created successfully'


class ContactUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contact
    fields = ['first_name', 'last_name', 'birthday']
    template_name = 'update_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Contact (%(first_name)s %(last_name)s) was updated successfully'


class PhoneUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Phone
    fields = ['phone_number']
    template_name = 'update_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Phone (%(phone_number)s) was updated successfully'


class AddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Address
    fields = ['address']
    template_name = 'update_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Address (%(address)s) was updated successfully'


class EmailUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Email
    fields = ['email']
    template_name = 'update_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Email (%(email)s) was updated successfully'


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'delete_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Contact (%(first_name)s %(last_name)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(ContactDeleteView, self).delete(request, *args, **kwargs)


class PhoneDeleteView(LoginRequiredMixin, DeleteView):
    model = Phone
    template_name = 'delete_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Phone (%(phone_number)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(PhoneDeleteView, self).delete(request, *args, **kwargs)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = 'delete_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Address (%(address)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(AddressDeleteView, self).delete(request, *args, **kwargs)


class EmailDeleteView(LoginRequiredMixin, DeleteView):
    model = Email
    template_name = 'delete_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Email (%(email)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(EmailDeleteView, self).delete(request, *args, **kwargs)


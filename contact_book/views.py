from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from contact_book.filters import ContactFilter
from contact_book.forms import ContactAddForm, PhoneAddForm, EmailAddressForm
from contact_book.models import Contact, Phone, Address, Email
from django.contrib import messages


@login_required
def contact_add(request):
    form = ContactAddForm(request.POST)
    form_phone = PhoneAddForm(request.POST)
    form_email_address = EmailAddressForm(request.POST)
    if request.method == 'POST':
        if form.is_valid() and form_phone.is_valid() and form_email_address.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            form_phone = form_phone.save(commit=False)
            form_phone.contact = form
            form_phone.user = request.user
            form_phone.save()
            email = form_email_address.cleaned_data['email']
            address = form_email_address.cleaned_data['address']
            if email:
                Email.objects.create(email=email, contact=form, user=request.user)
            if address:
                Address.objects.create(address=address, contact=form, user=request.user)
            messages.success(request, 'Contact was created successfully')
            return redirect('home')
    else:
        form = ContactAddForm()
        form_phone = PhoneAddForm()
        form_email_address = EmailAddressForm()
    return render(request, 'contact_form.html', {'form': form, 'form_phone': form_phone,
                                                 'form_email_address': form_email_address})


class HomePageView(LoginRequiredMixin, ListView):
    template_name = 'home.html'
    paginate_by = 10
    model = Contact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ContactFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        qs = self.model.objects.filter(user=self.request.user).order_by('last_name')
        contacts = ContactFilter(self.request.GET, queryset=qs)
        return contacts.qs


class ContactAddMixin(object):

    def form_valid(self, form):
        obj = form.save(commit=False)
        contact = Contact.objects.get(id=self.kwargs['pk'])
        if contact.user == self.request.user:
            obj.contact = Contact.objects.get(id=self.kwargs['pk'])
            obj.user = self.request.user
            form.save()
        else:
            raise PermissionDenied
        return super(ContactAddMixin, self).form_valid(form)


class UserAccessTestMixin(object):

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class PhoneAddView(LoginRequiredMixin, ContactAddMixin, SuccessMessageMixin, CreateView):
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


class ContactView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Contact
    form_class = ContactAddForm
    template_name = 'update_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Contact (%(first_name)s %(last_name)s) was updated successfully'


class PhoneView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Phone
    fields = ['phone_number']
    template_name = 'update_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Phone (%(phone_number)s) was updated successfully'


class AddressView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Address
    fields = ['address']
    template_name = 'update_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Address (%(address)s) was updated successfully'


class EmailView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Email
    fields = ['email']
    template_name = 'update_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Email (%(email)s) was updated successfully'


class ContactDeleteView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, DeleteView):
    model = Contact
    template_name = 'delete_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Contact (%(first_name)s %(last_name)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(ContactDeleteView, self).delete(request, *args, **kwargs)


class PhoneDeleteView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, DeleteView):
    model = Phone
    template_name = 'delete_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Phone (%(phone_number)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(PhoneDeleteView, self).delete(request, *args, **kwargs)


class AddressDeleteView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, DeleteView):
    model = Address
    template_name = 'delete_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Address (%(address)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(AddressDeleteView, self).delete(request, *args, **kwargs)


class EmailDeleteView(LoginRequiredMixin, UserAccessTestMixin, UserPassesTestMixin, DeleteView):
    model = Email
    template_name = 'delete_form.html'
    success_url = reverse_lazy('home')
    success_message = 'Email (%(email)s) was deleted successfully'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(EmailDeleteView, self).delete(request, *args, **kwargs)


def custom_page_not_found_view(request, exception):
    user = request.user
    return render(request, "errors/404.html", {'user': user})


def custom_error_view(request, exception=None):
    user = request.user
    return render(request, "errors/500.html", {'user': user})


def custom_permission_denied_view(request, exception=None):
    user = request.user
    return render(request, "errors/403.html", {'user': user})


def custom_bad_request_view(request, exception=None):
    user = request.user
    return render(request, "errors/400.html", {'user': user})

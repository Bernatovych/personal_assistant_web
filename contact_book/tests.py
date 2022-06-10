import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse, resolve
from django.template import Context, Template
from accounts.models import Profile
from .forms import ContactAddForm, PhoneAddForm, EmailAddressForm
from .models import Contact, Phone, Email, Address
from .views import contact_add, PhoneAddView, EmailAddView, AddressAddView, ContactUpdateView, PhoneUpdateView, \
    EmailUpdateView, AddressUpdateView, ContactDeleteView, PhoneDeleteView, EmailDeleteView, AddressDeleteView


class ContactListTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.client.login(username='test', password='test_user')
        notes = 11
        for i in range(notes):
            Contact.objects.create(first_name=f'Test {i}', last_name='Test', birthday='1900-01-01', user=self.user)

    def test_home_list_view_success_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_list_pagination_is_ten(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['page_obj']) == 10)

    def test_home_list_second_page(self):
        resp = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['page_obj']) == 1)


class NewContactTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.client.login(username='test', password='test_user')

    def test_new_contact_view_success_status_code(self):
        url = reverse('contact_add')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_contact_url_resolves_new_contact_view(self):
        view = resolve('/contact_add/')
        self.assertEquals(view.func, contact_add)

    def test_csrf(self):
        url = reverse('contact_add')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        url = reverse('contact_add')
        response = self.client.get(url)
        form = response.context.get('form')
        form_phone = response.context.get('form_phone')
        form_email_address = response.context.get('form_email_address')
        self.assertIsInstance(form, ContactAddForm)
        self.assertIsInstance(form_phone, PhoneAddForm)
        self.assertIsInstance(form_email_address, EmailAddressForm)

    def test_new_contact_valid_post_data(self):
        self.client.login(username='test', password='test_user')
        url = reverse('contact_add')
        data = {
            'first_name': 'Test',
            'last_name': 'Tests',
            'birthday': '1900-01-01',
            'phone_number': '+390631111111',
            'email': 'test@test.ua',
            'address': 'test, 70',
        }
        self.client.post(url, data)
        self.assertTrue(Contact.objects.exists())
        self.assertTrue(Phone.objects.exists())
        self.assertTrue(Email.objects.exists())
        self.assertTrue(Address.objects.exists())

    def test_new_contact_without_email_address_valid_post_data(self):
        self.client.login(username='test', password='test_user')
        url = reverse('contact_add')
        data = {
            'first_name': 'Test',
            'last_name': 'Tests',
            'birthday': '1900-01-01',
            'phone_number': '+390631111111',
            'email': '',
            'address': '',
        }
        self.client.post(url, data)
        self.assertTrue(Contact.objects.exists())
        self.assertTrue(Phone.objects.exists())
        self.assertFalse(Email.objects.exists())
        self.assertFalse(Address.objects.exists())

    def test_new_contact_invalid_post_data(self):
        url = reverse('contact_add')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_contact_invalid_post_data_empty_fields(self):
        url = reverse('contact_add')
        data = {'text': '', 'tag': ''}
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Contact.objects.exists())
        self.assertFalse(Phone.objects.exists())
        self.assertFalse(Email.objects.exists())
        self.assertFalse(Address.objects.exists())


class NewPhoneTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        contact = Contact.objects.create(first_name='Test', last_name='Test', birthday='1900-01-01', user=self.user)
        Phone.objects.create(phone_number='+380631111111', contact=contact)
        self.client.login(username='test', password='test_user')

    def test_new_phone_view_success_status_code(self):
        url = reverse('phone_add', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_phone_url_resolves_new_phone_view(self):
        view = resolve('/phone_add/1/')
        self.assertEquals(view.func.view_class, PhoneAddView)

    def test_csrf(self):
        url = reverse('phone_add', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_phone_valid_post_data(self):
        url = reverse('phone_add', kwargs={'pk': 1})
        data = {'phone_number': '+380631111112'}
        self.client.post(url, data)
        self.assertTrue(Phone.objects.exists())

    def test_new_phone_invalid_post_data(self):
        url = reverse('phone_add', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_phone_invalid_post_data_empty_fields(self):
        url = reverse('phone_add', kwargs={'pk': 1})
        data = {'phone_number': ''}
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_phone_invalid_phone_exist_data(self):
        url = reverse('phone_add', kwargs={'pk': 1})
        data = {'phone_number': '+380631111111'}
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_phone_invalid_phone_data(self):
        url = reverse('phone_add', kwargs={'pk': 1})
        data = {'phone_number': '+380631111'}
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)


class NewEmailTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        Contact.objects.create(first_name='Test', last_name='Test', birthday='1900-01-01', user=self.user)
        self.client.login(username='test', password='test_user')

    def test_new_email_view_success_status_code(self):
        url = reverse('email_add', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_email_url_resolves_new_email_view(self):
        view = resolve('/email_add/1/')
        self.assertEquals(view.func.view_class, EmailAddView)

    def test_csrf(self):
        url = reverse('email_add', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_email_valid_post_data(self):
        url = reverse('email_add', kwargs={'pk': 1})
        data = {'email': 'test@test.ua'}
        self.client.post(url, data)
        self.assertTrue(Email.objects.exists())

    def test_new_email_invalid_post_data(self):
        url = reverse('email_add', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_email_invalid_post_data_empty_fields(self):
        url = reverse('email_add', kwargs={'pk': 1})
        data = {'email': ''}
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_email_invalid_email_data(self):
        url = reverse('email_add', kwargs={'pk': 1})
        data = {'phone_number': 'test@test'}
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)


class NewAddressTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        Contact.objects.create(first_name='Test', last_name='Test', birthday='1900-01-01', user=self.user)
        self.client.login(username='test', password='test_user')

    def test_new_address_view_success_status_code(self):
        url = reverse('address_add', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_address_url_resolves_new_email_view(self):
        view = resolve('/address_add/1/')
        self.assertEquals(view.func.view_class, AddressAddView)

    def test_csrf(self):
        url = reverse('address_add', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_address_valid_post_data(self):
        url = reverse('address_add', kwargs={'pk': 1})
        data = {'address': 'test'}
        self.client.post(url, data)
        self.assertTrue(Address.objects.exists())

    def test_new_address_invalid_post_data(self):
        url = reverse('address_add', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_address_invalid_post_data_empty_fields(self):
        url = reverse('address_add', kwargs={'pk': 1})
        data = {'address': ''}
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)


class UpdateViewTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.contact = Contact.objects.create(first_name='Test', last_name='Test', birthday='1900-01-01',
                                              user=self.user)
        self.phone = Phone.objects.create(phone_number='+380631111111', contact=self.contact)
        self.email = Email.objects.create(email='test@test.ua', contact=self.contact)
        self.address = Address.objects.create(address='test, 70', contact=self.contact)
        self.contact_url = reverse('contact_update', kwargs={'pk': self.contact.pk})
        self.phone_url = reverse('phone_update', kwargs={'pk': self.phone.pk})
        self.email_url = reverse('email_update', kwargs={'pk': self.email.pk})
        self.address_url = reverse('address_update', kwargs={'pk': self.address.pk})


class ContactUpdateViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.contact_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/contact_update/1/')
        self.assertEquals(view.func.view_class, ContactUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)


class SuccessfulContactUpdateViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.contact_url,
                                         {'first_name': 'Test1', 'last_name': 'Tests1', 'birthday': '1900-01-02'})

    def test_redirection(self):
        home_url = reverse('home')
        self.assertRedirects(self.response, home_url)

    def test_contact_changed(self):
        self.contact.refresh_from_db()
        self.assertEquals(self.contact.first_name, 'Test1')
        self.assertEquals(self.contact.last_name, 'Tests1')
        self.assertEquals(self.contact.birthday, datetime.date(1900, 1, 2))


class InvalidContactUpdateViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.contact_url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)


class PhoneUpdateViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.phone_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/phone_update/1/')
        self.assertEquals(view.func.view_class, PhoneUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)


class SuccessfulPhoneUpdateViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.phone_url, {'phone_number': '+380631111112'})

    def test_redirection(self):
        home_url = reverse('home')
        self.assertRedirects(self.response, home_url)

    def test_phone_changed(self):
        self.phone.refresh_from_db()
        self.assertEquals(self.phone.phone_number, '+380631111112')


class InvalidPhoneUpdateViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.phone_url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)


class InvalidPhoneUpdateDataViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.phone_url, {'phone_number': '+380631111'})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)


class EmailUpdateViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.email_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/email_update/1/')
        self.assertEquals(view.func.view_class, EmailUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)


class SuccessfulEmailUpdateViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.email_url, {'email': 'test1@test.ua'})

    def test_redirection(self):
        home_url = reverse('home')
        self.assertRedirects(self.response, home_url)

    def test_email_changed(self):
        self.email.refresh_from_db()
        self.assertEquals(self.email.email, 'test1@test.ua')


class InvalidEmailUpdateViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.email_url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)


class InvalidEmailUpdateDataViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.email_url, {'email': 'test.test.ua'})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)


class AddressUpdateViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.address_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/address_update/1/')
        self.assertEquals(view.func.view_class, AddressUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)


class SuccessfulAddressUpdateViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.address_url, {'address': 'test, 71'})

    def test_redirection(self):
        home_url = reverse('home')
        self.assertRedirects(self.response, home_url)

    def test_email_changed(self):
        self.address.refresh_from_db()
        self.assertEquals(self.address.address, 'test, 71')


class InvalidAddressUpdateViewTests(UpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.address_url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)


class DeleteViewTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.contact = Contact.objects.create(first_name='Test', last_name='Test', birthday='1900-01-01',
                                              user=self.user)
        self.phone = Phone.objects.create(phone_number='+380631111111', contact=self.contact)
        self.email = Email.objects.create(email='test@test.ua', contact=self.contact)
        self.address = Address.objects.create(address='test, 70', contact=self.contact)
        self.contact_url = reverse('contact_delete', kwargs={'pk': self.contact.pk})
        self.phone_url = reverse('phone_delete', kwargs={'pk': self.phone.pk})
        self.email_url = reverse('email_delete', kwargs={'pk': self.email.pk})
        self.address_url = reverse('address_delete', kwargs={'pk': self.address.pk})


class ContactDeleteViewTests(DeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.contact_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/contact_delete/1/')
        self.assertEquals(view.func.view_class, ContactDeleteView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)

    def test_contact_get_request(self):
        response = self.client.get(reverse('contact_delete', args=(self.contact.id,)), follow=True)
        self.assertContains(response, 'Are you sure you want to delete "Test Test"?')


class PhoneDeleteViewTests(DeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.phone_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/phone_delete/1/')
        self.assertEquals(view.func.view_class, PhoneDeleteView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)

    def test_contact_get_request(self):
        response = self.client.get(reverse('phone_delete', args=(self.phone.id,)), follow=True)
        self.assertContains(response, 'Are you sure you want to delete "+380631111111"?')


class EmailDeleteViewTests(DeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.email_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/email_delete/1/')
        self.assertEquals(view.func.view_class, EmailDeleteView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)

    def test_contact_get_request(self):
        response = self.client.get(reverse('email_delete', args=(self.email.id,)), follow=True)
        self.assertContains(response, 'Are you sure you want to delete "test@test.ua"?')


class AddressDeleteViewTests(DeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.address_url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/address_delete/1/')
        self.assertEquals(view.func.view_class, AddressDeleteView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)

    def test_contact_get_request(self):
        response = self.client.get(reverse('address_delete', args=(self.email.id,)), follow=True)
        self.assertContains(response, 'Are you sure you want to delete "test, 70"?')


class TemplateTagTest(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.client.login(username='test', password='test_user')
        self.profile = Profile.objects.get(user=self.user)
        today = datetime.date.today() + datetime.timedelta(days=6)
        self.birthday = today.strftime("%Y-%m-%d")
        Contact.objects.create(first_name='Test', last_name='Test', birthday=self.birthday, user=self.user)

    def test_render(self):
        context = Context({'title': f'Holidays in {self.profile.period} days', 'user': self.user})
        template_to_render = Template('{% load holidays_period_tag %}''{% holidays_period %}')
        rendered_template = template_to_render.render(context)
        self.assertInHTML('<h4>Holidays in 7 days</h4>', rendered_template)
        self.assertInHTML("<div><span class='text-danger'>6</span> days left: Test Test</div>", rendered_template)


class TemplateTagTest1(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.client.login(username='test', password='test_user')
        self.profile = Profile.objects.get(user=self.user)
        self.profile.period = 365
        self.profile.save()
        today = datetime.date.today() + datetime.timedelta(days=-4)
        self.birthday = today.strftime("%Y-%m-%d")
        Contact.objects.create(first_name='Test', last_name='Test', birthday=self.birthday, user=self.user)

    def test_render(self):
        context = Context({'title': f'Holidays in {self.profile.period} days', 'user': self.user})
        template_to_render = Template('{% load holidays_period_tag %}''{% holidays_period %}')
        rendered_template = template_to_render.render(context)
        self.assertInHTML('<h4>Holidays in 365 days</h4>', rendered_template)
        self.assertInHTML("<div><span class='text-danger'>361</span> days left: Test Test</div>", rendered_template)
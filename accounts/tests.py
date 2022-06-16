from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.forms import ModelForm
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import Profile
from .views import UserSignUpView, profile_update


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEquals(view.func.view_class, UserSignUpView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)


class SuccessfulSignUpEmailSentTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'test',
            'email': 'test@test.ua',
            'password1': 'test_user',
            'password2': 'test_user'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('account_activation_sent')

    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/password_reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="submit"', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'test@test.ua'
        User.objects.create_user(username='test', email=email, password='test_user')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'test@test.ua'})

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))


class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='test', email='test@test.ua', password='test_user')
        self.response = self.client.post(reverse('password_reset'), {'email': 'test@test.ua'})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('Скидання пароля на testserver', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid, 'token': token})
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('test', self.email.body)
        self.assertIn('test@test.ua', self.email.body)

    def test_email_to(self):
        self.assertEqual(['test@test.ua'], self.email.to)


class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)


class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', email='test@test.ua', password='test_user')
        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).encode().decode()
        self.token = default_token_generator.make_token(user)

        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        print(url)
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/reset/{uidb64}/{token}'.format(uidb64=self.uid, token=self.token))
        self.assertEquals(view.func.view_class, PasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 2)
        self.assertContains(self.response, 'type="submit"', 1)


class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', email='test@test.ua', password='test_user')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).encode().decode()
        token = default_token_generator.make_token(user)
        user.set_password('user_test')
        user.save()

        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))


class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)


class ProfileUpdateViewTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.profile = Profile.objects.get(user=self.user)
        self.url = reverse('profile_update', kwargs={'pk': self.profile.pk})


class ProfileUpdateViewTests(ProfileUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/accounts/profile_update/1/')
        self.assertEquals(view.func, profile_update)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 7)


class SuccessfulProfileUpdateViewTests(ProfileUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'username': 'Test1', 'email': 'test1@test.com',
                                                    'period': 8, 'is_news': 'True', 'is_weather': 'True',
                                                    'is_football': 'True'})

    def test_redirection(self):
        note_book_url = reverse('home')
        self.assertRedirects(self.response, note_book_url)

    def test_profile_changed(self):
        self.profile.refresh_from_db()
        self.assertEquals(self.profile.user.username, 'Test1')
        self.assertEquals(self.profile.user.email, 'test1@test.com')
        self.assertEquals(self.profile.period, 8)
        self.assertEquals(self.profile.is_news, True)
        self.assertEquals(self.profile.is_weather, True)
        self.assertEquals(self.profile.is_football, True)


class InvalidProfileUpdateViewTests(ProfileUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

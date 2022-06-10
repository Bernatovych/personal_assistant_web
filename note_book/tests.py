from django.contrib.auth.models import User
from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse, resolve
from .forms import NoteAddForm, TagAddForm
from .models import Note, Tag
from .views import NoteUpdateView, TagUpdateView, note_add, TagAddView, NoteDeleteView, TagDeleteView


class NoteListTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.client.login(username='test', password='test_user')
        notes = 11
        for i in range(notes):
            Note.objects.create(text=f'Test {i}', user=self.user)

    def test_note_list_view_success_status_code(self):
        url = reverse('note_book')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_note_list_pagination_is_ten(self):
        resp = self.client.get(reverse('note_book'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['page_obj']) == 10)

    def test_note_list_second_page(self):
        resp = self.client.get(reverse('note_book') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['page_obj']) == 1)


class NewNoteTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.client.login(username='test', password='test_user')

    def test_new_note_view_success_status_code(self):
        url = reverse('note_add')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_note_url_resolves_new_note_view(self):
        view = resolve('/note_book/note_add/')
        self.assertEquals(view.func, note_add)

    def test_csrf(self):
        url = reverse('note_add')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        url = reverse('note_add')
        response = self.client.get(url)
        form = response.context.get('form')
        form_tag = response.context.get('form_tag')
        self.assertIsInstance(form, NoteAddForm)
        self.assertIsInstance(form_tag, TagAddForm)

    def test_new_note_valid_post_data(self):
        self.client.login(username='test', password='test_user')
        url = reverse('note_add')
        data = {'text': 'test', 'tag': 'tag'}
        self.client.post(url, data)
        self.assertTrue(Note.objects.exists())
        self.assertTrue(Tag.objects.exists())

    def test_new_note_without_tag_valid_post_data(self):
        self.client.login(username='test', password='test_user')
        url = reverse('note_add')
        data = {'text': 'test', 'tag': ''}
        self.client.post(url, data)
        self.assertTrue(Note.objects.exists())
        self.assertFalse(Tag.objects.exists())

    def test_new_note_invalid_post_data(self):
        url = reverse('note_add')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_note_invalid_post_data_empty_fields(self):
        url = reverse('note_add')
        data = {'text': '', 'tag': ''}
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Note.objects.exists())
        self.assertFalse(Tag.objects.exists())


class NewTagTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        self.user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.note = Note.objects.create(text='text', user=self.user)
        self.client.login(username='test', password='test_user')

    def test_new_tag_view_success_status_code(self):
        url = reverse('tag_add', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_tag_url_resolves_new_note_view(self):
        view = resolve('/note_book/tag_add/1/')
        self.assertEquals(view.func.view_class, TagAddView)

    def test_csrf(self):
        url = reverse('tag_add', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_tag_valid_post_data(self):
        url = reverse('tag_add', kwargs={'pk': 1})
        data = {'tag': 'test'}
        self.client.post(url, data)
        self.assertTrue(Tag.objects.exists())

    def test_new_tag_invalid_post_data(self):
        url = reverse('tag_add', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_tag_invalid_post_data_empty_fields(self):
        url = reverse('tag_add', kwargs={'pk': 1})
        data = {'text': ''}
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Tag.objects.exists())


class NoteUpdateViewTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.note = Note.objects.create(text='text', user=user)
        self.url = reverse('note_update', kwargs={'pk': self.note.pk})


class NoteUpdateViewTests(NoteUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/note_book/note_update/1/')
        self.assertEquals(view.func.view_class, NoteUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulNoteUpdateViewTests(NoteUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'text': 'edited text'})

    def test_redirection(self):
        note_book_url = reverse('note_book')
        self.assertRedirects(self.response, note_book_url)

    def test_note_changed(self):
        self.note.refresh_from_db()
        self.assertEquals(self.note.text, 'edited text')


class InvalidNoteUpdateViewTests(NoteUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)


class TagUpdateViewTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.note = Note.objects.create(text='text', user=user)
        self.tag = Tag.objects.create(tag='tag', note=self.note)
        self.url = reverse('tag_update', kwargs={'pk': self.tag.pk})


class TagUpdateViewTests(TagUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/note_book/tag_update/1/')
        self.assertEquals(view.func.view_class, TagUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)


class SuccessfulTagUpdateViewTests(TagUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'tag': 'edited tag'})

    def test_redirection(self):
        note_book_url = reverse('note_book')
        self.assertRedirects(self.response, note_book_url)

    def test_tag_changed(self):
        self.tag.refresh_from_db()
        self.assertEquals(self.tag.tag, 'edited tag')


class InvalidTagUpdateViewTests(TagUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)


class NoteDeleteViewTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.note = Note.objects.create(text='text', user=user)
        self.url = reverse('note_delete', kwargs={'pk': self.note.pk})


class NoteDeleteViewTests(NoteDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/note_book/note_delete/1/')
        self.assertEquals(view.func.view_class, NoteDeleteView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)

    def test_tag_get_request(self):
        response = self.client.get(reverse('note_delete', args=(self.note.id,)), follow=True)
        self.assertContains(response, 'Are you sure you want to delete "text"?')


class TagDeleteViewTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test_user'
        user = User.objects.create_user(username=self.username, email='test@test.com', password=self.password)
        self.note = Note.objects.create(text='text', user=user)
        self.tag = Tag.objects.create(tag='tag', note=self.note)
        self.url = reverse('tag_delete', kwargs={'pk': self.tag.pk})


class TagDeleteViewTests(TagDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/note_book/tag_delete/1/')
        self.assertEquals(view.func.view_class, TagDeleteView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)

    def test_tag_get_request(self):
        self.response = self.client.get(reverse('tag_delete', args=(self.tag.id,)), follow=True)
        self.assertContains(self.response, 'Are you sure you want to delete "tag"?')
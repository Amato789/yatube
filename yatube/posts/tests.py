from django.contrib.auth.models import User
from django.test import TestCase, Client
from .models import Group, Post


class TestIndexPage(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_index_available(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class TestGroups(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def tearDown(self) -> None:
        Group.objects.filter(slug='test_slug').delete()

    def test_page_not_found(self):
        response = self.client.get('/group/not_exist/')
        self.assertEqual(response.status_code, 404)

    def test_exists_groups(self):
        Group.objects.create(
            title='test_title',
            slug='test_slug',
            description='test_description'
        )
        response = self.client.get('/group/test_slug/')
        self.assertEqual(response.status_code, 200)


class TestPosts(TestCase):
    def setUp(self) -> None:
        self.auth_client = Client()
        user = User.objects.create(username='test_user', email='test_email')
        user.set_password('123')
        user.save()
        self.auth_client.login(username='test_user', password='123')
        print('Start setUp')

    def tearDown(self) -> None:
        Group.objects.filter(
            title='test_title',
            slug='test_slug',
            description='test_description'
        ).delete()
        User.objects.filter(username='test_user').delete()
        print('Start tearDown')

    def test_valid_form(self):
        group = Group.objects.create(
            title='test_title',
            slug='test_slug',
            description='test_description'
        )
        group_id = f'{group.id}'
        self.auth_client.post('/new/', data={'text': 'testing valid form', 'group': group_id})
        self.assertTrue(Post.objects.filter(text='testing valid form', group=group_id).exists())

    def test_not_valid_form(self):
        response = self.auth_client.post('/new/', data={'group': '100200'})
        self.assertFormError(response, form='form', field='text', errors=['Обязательное поле.'])
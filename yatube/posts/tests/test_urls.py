import http

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group


User = get_user_model()


STATUS_CODE = http.HTTPStatus.OK


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            id='1'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='IgorKorovin')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_of_accessible_pages(self):
        template_pages = [
            '/',
            '/group/test-slug/',
            '/profile/IgorKorovin/',
            '/posts/1/'
        ]
        for template in template_pages:
            with self.subTest(template):
                response = self.guest_client.get(template)
                self.assertEqual(response.status_code, STATUS_CODE)

    def test_inaccessible_pages(self):
        status_code = http.HTTPStatus.BAD_REQUEST
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, status_code)

    def test_unauthorized_page_create(self):
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_authorized_pages(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, STATUS_CODE)

    def test_unauthorized_page_edit(self):
        response = self.guest_client.get('/posts/1/edit/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/posts/1/edit/')

    def test_only_author_pages(self):
        response = self.client.get('/posts/1/edit/', follow=True)
        self.assertEqual(response.status_code, STATUS_CODE)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/IgorKorovin/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            '/posts/1/edit/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

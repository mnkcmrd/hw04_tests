from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group
from ..forms import PostForm

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            id=1,
            group=Group.objects.create(
                title='test_group_title',
                slug='test_group_slug'
            )
        )
        cls.form = PostForm()

    def setUp(self):
        self.user = User.objects.create_user(username='IgorKorovin')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост'
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.user})
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(response.status_code, 200)

    def test_edit_post(self):
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост'
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(response.status_code, 200)

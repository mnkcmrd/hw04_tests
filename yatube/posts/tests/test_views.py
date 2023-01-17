from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms


from ..models import Group, Post

User = get_user_model()


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
            id=1,
            group=Group.objects.create(
                title='test_group_title',
                slug='test_group_slug'
            )
        )

    def setUp(self):
        self.user = User.objects.create_user(username='IgorKorovin')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={
                'slug': 'test-slug'
            }): 'posts/group_list.html',
            reverse('posts:profile', kwargs={
                'username': self.user
            }): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={
                'post_id': '1'
            }): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={
                'post_id': '1'
            }): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html'
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        page_object = response.context['page_obj'][0]
        post = page_object.text
        self.assertEqual(post, self.post.text)

    def test_group_list_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.post.group.slug}
            )
        )
        page_object = response.context['page_obj'][0]
        post = page_object.text
        self.assertEqual(post, self.post.text)

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.post.author}
            )
        )
        page_object = response.context['page_obj'][0]
        post = page_object.text
        self.assertEqual(post, self.post.text)

    def test_post_detail_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            )
        )
        self.assertEqual(
            response.context.get('post').text,
            self.post.text
        )

    def test_post_edit_page_filter_id(self):
        response = self.authorized_client.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}
            )
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_create_page_filter_id(self):
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_create_in_index_group_profile_page(self):
        responses = [
            self.authorized_client.get(reverse('posts:index')),
            self.authorized_client.get(reverse('posts:group_list', kwargs={'slug': self.post.group.slug})),
            self.authorized_client.get(reverse('posts:profile', kwargs={'username': self.post.author}))
        ]
        for response in responses:
            self.assertEqual(response.context.get('page_obj')[0].text, self.post.text)
            self.assertEqual(response.context.get('page_obj')[0].group, self.post.group)
            self.assertEqual(response.context.get('page_obj')[0].id, self.post.id)
            self.assertNotEqual(response.context.get('page_obj')[0].group, self.group)


class PaginatorViewsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.posts_bulk = Post.objects.bulk_create(
            Post(
                text=f'Тестовый текст {i}',
                author=cls.user,
                group=cls.group
            ) for i in range(13)
        )

    def setUp(self):
        self.user = User.objects.create_user(username='IgorKorovin')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        responses = [
            self.client.get(reverse('posts:index')),
            self.client.get(reverse('posts:group_list', kwargs={'slug': self.group.slug})),
            self.client.get(reverse('posts:profile', kwargs={'username': 'auth'}))
        ]
        for response in responses:
            self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        responses = [
            self.client.get(reverse('posts:index') + '?page=2'),
            self.client.get(reverse('posts:group_list', kwargs={'slug': self.group.slug}) + '?page=2'),
            self.client.get(reverse('posts:profile', kwargs={'username': 'auth'}) + '?page=2')
        ]
        for response in responses:
            self.assertEqual(len(response.context['page_obj']), 3)


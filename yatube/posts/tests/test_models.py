from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Post, Group


User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_text_length(self):
        post = PostModelTest.post
        text_length = post.text
        self.assertEqual(text_length, post.text[:15])

    def test_group_title_label(self):
        group = PostModelTest.group
        group_title = group.title
        self.assertEqual(group_title, 'Тестовая группа')

    def test_object_name_is_title_fild(self):
        group = PostModelTest.group
        group_title = group.title
        self.assertEqual(group_title, str(group))

    def test_object_name_is_text_fild(self):
        post = PostModelTest.post
        post_text = post.text
        self.assertEqual(post.text, str(post))
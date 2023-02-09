from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts'
    )

    group = models.ForeignKey(
        'Group',
        verbose_name='Группа',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    image = models.ImageField(
        'Image',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


# Create your models here.

class Post(models.Model):

    STATUS_CHOICES = (('draft', 'Wersja robocza'),
                      ('published', 'Opublikowany'),)

    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    slug = models.SlugField(max_length=250, unique_for_date='publish')

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                        self.publish.month,
                                        self.publish.day,
                                        self.slug])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-publish',)

class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')

    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Komentarz dodany przez {self.name} dla posta {self.post}'
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Page(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    liked = models.ManyToManyField(User, related_name='liked', default=None, blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        default='photos/default.jpg',
        blank=True,
        verbose_name='Фото')
    age = models.IntegerField(verbose_name='Возраст')

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    @property
    def num_likes(self):
        return self.liked.all().count()

    def get_absolute_url(self):
        return reverse('view_page', kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.user)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
)


class Relationship(models.Model):
    sender = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"






from django.db import models
from django.urls import reverse


class Page(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    age = models.IntegerField(verbose_name='Возраст')
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('home', kwargs={"pk": self.pk})

    def __str__(self):
        return self.last_name


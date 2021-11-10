from django.db import models
from django.urls import reverse

class Souvenir(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    price = models.IntegerField(verbose_name="Цена")
    availability = models.BooleanField(default=False, verbose_name="Наличие")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории", related_name='get_goods')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('goods', kwargs={'goods_slug': self.slug})

    class Meta:
        verbose_name = "Сувенир"
        verbose_name_plural = "Сувениры"
        # ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"
        ordering = ['name']
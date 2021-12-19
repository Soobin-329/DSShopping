from django.db import models
from django.contrib.auth.models import User
import os
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/mall/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'


class Maker(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)

    logo = models.ImageField(upload_to='maker/images/%Y/%m/', blank=True)

#    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/mall/maker/{self.pk}'

class Product(models.Model):
    name = models.CharField(max_length=100)
    content = MarkdownxField()
    price = models.IntegerField()
    material = models.CharField(max_length=100, blank=True)

    image = models.ImageField(upload_to='mall/images/%Y/%m/%d/', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    maker = models.ForeignKey(Maker, null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):
        return f'[{self.pk}]{self.name} :: {self.category}'

    def get_absolute_url(self):
        return f'/mall/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.content)

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.product.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists() :
            return self.author.socialaccount_set.first().get_avatar_url()
        else :
            return 'https://doitdjango.com/avatar/id/396/c5a7816bd8149d0b/svg/{self.author.email}/'


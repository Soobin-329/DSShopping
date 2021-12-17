from django.db import models

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
    content = models.CharField(max_length=100, blank=True)
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



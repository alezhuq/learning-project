from django.db import models


# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=32, verbose_name="news title")
    content = models.TextField(blank=True, verbose_name="news content")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank="True")
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = "news"
        verbose_name_plural = "news"
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name="category name")

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['title']

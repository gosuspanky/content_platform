from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from transliterate import translit

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class Comment(models.Model):
    comment = models.TextField(verbose_name='Comment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created date')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.comment


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)
    image = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Image')
    description = models.TextField(verbose_name='Description', **NULLABLE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Updated at', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User', **NULLABLE)
    published_on = models.BooleanField(default=False, verbose_name='Published on')
    views = models.IntegerField(default=0, verbose_name='Views', **NULLABLE)
    price = models.IntegerField(default=0, verbose_name='Price')
    is_paid = models.BooleanField(default=False, verbose_name='Is paid')
    comments = models.ManyToManyField(Comment, verbose_name='Comments', blank=True)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Save the object with an automatically generated slug if none is provided.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.slug:
            transliterated_title = translit(self.title, 'ru', reversed=True)
            self.slug = slugify(transliterated_title, allow_unicode=True)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})

    def toggle_published(self):
        """
        Toggles the published status of the object and saves the changes.
        """
        self.published_on = not self.published_on
        self.save()

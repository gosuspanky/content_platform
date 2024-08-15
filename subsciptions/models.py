from django.db import models

from blog.models import Blog, NULLABLE
from users.models import User


# Create your models here.


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='Blog')
    status = models.BooleanField(default=False, verbose_name='Status')
    payment_status = models.BooleanField(default=False, verbose_name='Payment status')
    payment_date = models.DateTimeField(auto_now=True, verbose_name='Payment date', **NULLABLE)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f'{self.user} - {self.blog}: {self.status}'

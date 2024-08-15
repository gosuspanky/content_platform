from django.contrib import admin

from subsciptions.models import Subscription


# Register your models here.


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "blog", "status", "payment_status", "payment_date")

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

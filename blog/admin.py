from django.contrib import admin

from blog.models import Blog, Comment


# Register your models here.


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
        "published_on",
        "price",
        "is_paid",
        "created_date",
        "updated_date",
    )
    prepopulated_fields = {"slug": ("title",)}

    def republish(self, request, queryset):
        """
        Republishes items in the queryset by updating their published_on field and notifies the user.
        :param request: The request object
        :param queryset: The queryset of items to republish
        :return: None
        """
        queryset.update(published_on=True)
        self.message_user(request, "Successfully republished")

    republish.short_description = "Republish"
    actions = ["republish"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "user", "created_date")
    list_filter = ("user", "created_date")

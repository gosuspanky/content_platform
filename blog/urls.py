from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import (
    HomePageView,
    BlogListView,
    BlogCreateView,
    BlogDetailView,
    BlogUpdateView,
    BlogDeleteView,
    toggle_activity,
)

app_name = BlogConfig.name

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("blog/", cache_page(60)(BlogListView.as_view()), name="blog_list"),
    path("blog/create/", BlogCreateView.as_view(), name="blog_create"),
    path("blog/<slug:slug>/", BlogDetailView.as_view(), name="blog_detail"),
    path("blog/update/<slug:slug>/", BlogUpdateView.as_view(), name="blog_update"),
    path("blog/delete/<slug:slug>/", BlogDeleteView.as_view(), name="blog_delete"),
    path("blog/toggle_activity/<slug:slug>/", toggle_activity, name="toggle_activity"),
]

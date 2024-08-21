from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from blog.forms import BlogForm, CommentForm
from blog.models import Blog, Comment
from subsciptions.models import Subscription


# Create your views here.


class HomePageView(TemplateView):
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        """
        Generate context data for the view with information about blogs.

        Parameters:
            **kwargs (dict): Additional keyword arguments.

        Returns:
            dict: A dictionary containing context data for the view.
        """
        context_data = super().get_context_data(**kwargs)
        context_data["blog"] = Blog.objects.filter(published_on=True).order_by("?")[:3]

        if self.request.user.is_authenticated:
            user = self.request.user

            subscribed_blog_ids = Subscription.objects.filter(
                user=user, status=True
            ).values_list("blog__id", flat=True)

            unsubscribed_blogs = Blog.objects.filter(published_on=True).exclude(
                id__in=subscribed_blog_ids
            )
            subscribed_blogs = Blog.objects.filter(
                id__in=subscribed_blog_ids, published_on=True
            )

            context_data["unsubscribed_blogs"] = unsubscribed_blogs
            context_data["subscribed_blogs"] = subscribed_blogs

        return context_data


class BlogListView(LoginRequiredMixin, ListView):
    template_name = "blog/blog_list.html"
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published_on=True)
        return queryset


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = self.request.user
            blog.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    form_class = CommentForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["comments"] = Comment.objects.filter(blog=self.get_object())
        return context_data

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_content = form.cleaned_data["comment"]
            comment = Comment.objects.create(
                user=self.request.user, comment=comment_content
            )

            blog = self.get_object()
            blog.comments.add(comment)
            blog.save()
            return HttpResponseRedirect(self.request.path_info)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy("blog:blog_list")


def toggle_activity(slug):
    """
    Переключает атрибут 'published_on' объекта Blog.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        slug (str): Слаг объекта Blog.

    Returns:
        HttpResponseRedirect: Перенаправляет на страницу деталей объекта Blog.
    """
    record_item = get_object_or_404(Blog, slug=slug)
    record_item.toggle_published()
    # return HttpResponseRedirect(request.path_info)
    # return redirect(reverse("blog:blog_detail", args=[record_item.slug]))

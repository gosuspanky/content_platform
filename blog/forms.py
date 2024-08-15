from django import forms

from blog.models import Blog, Comment
from users.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'image', 'price', 'is_paid', 'published_on']
        exclude = ['user', 'slug', 'comment', 'views']


class CommentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

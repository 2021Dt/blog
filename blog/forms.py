from django import forms
from .models import Blog, BlogCategory, BlogComment


class PubBlogForm(forms.ModelForm):
    title = forms.CharField(max_length=200, min_length=2)
    content = forms.CharField(widget=forms.Textarea, min_length=2)
    category = forms.ModelChoiceField(queryset=BlogCategory.objects.all())

    class Meta:
        model = Blog
        fields = ['title', 'content', 'category']


class PubCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, min_length=2)

    class Meta:
        model = BlogComment
        fields = ['content']

from django import forms
from .models import BlogPost
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']

    content = forms.CharField(widget=CKEditorUploadingWidget())

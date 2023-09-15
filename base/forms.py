from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Category


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_photo = forms.ImageField(required=False)  # Add the profile_photo field

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'bio')


class CustomUserInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'status', 'bio', 'profile_picture')


from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({
            'rows': 3,
            'class': 'form-control',
        })


from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'scheduled_date', 'draft']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'draft': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class EditBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'scheduled_date', 'draft']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'draft': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class BlogPostFilterForm(forms.Form):
    title = forms.CharField(required=False)
    content = forms.CharField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="All", required=False)

from django import forms
from .models import Post, Tag, Comment


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={"placeholder": "제목을 입력하세요"}),
            'content': forms.Textarea(attrs={'id': 'content'})
        }


class TagForm(forms.ModelForm):
    
    class Meta:
        model = Tag
        fields = ['content']
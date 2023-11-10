from django import forms
from .models import Group, Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': ('Текс поста'),
            'group': ('Группа'),
        }
        help_texts = {
            'text': ('Удиви меня'),
            'group': ('Укажи группу')
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

from django import forms
from .models import Group, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': ('Текс поста'),
            'group': ('Группа'),
        }
        help_texts = {
            'text': ('Удиви меня'),
            'group': ('Укажи группу')
        }

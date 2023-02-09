from django.forms import ModelForm, forms
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

        def clean_subject(self):
            data = self.cleaned_data['text']
            if '' in data:
                raise forms.ValidationError('Поле должно быть заполнено')
            return data


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        def clean_subject(self):
            data = self.cleaned_data['text']
            if '' in data:
                raise forms.ValidationError('Поле должно быть заполнено')
            return data

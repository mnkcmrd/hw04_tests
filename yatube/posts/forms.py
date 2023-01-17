from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')

        def clean_subject(self):
            data = self.cleaned_data['text']
            if '' in data:
                raise forms.ValidationError('Поле должно быть заполнено')
            return data

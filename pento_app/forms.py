from django.contrib.auth import get_user_model
from django import forms
from .models import CustomUser
from .models import Post

User = get_user_model()

#プロフィール編集
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('username','description')
        help_texts = {
            'username': None,
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)


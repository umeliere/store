from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, FileInput, ImageField

from users.models import Profile


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")


class ProfileForm(ModelForm):
    photo = ImageField(required=False, label='Аватар', error_messages={'invalid': ('Только файлы изображений', )},
                       widget=FileInput)

    class Meta:
        model = Profile
        fields = ("address", "phone", "city", "photo")

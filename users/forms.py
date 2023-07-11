from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, FileInput, ImageField

from users.models import Profile


class UserForm(UserCreationForm):
    """
    Форма для регистрации пользователя
    """
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")


class ProfileUpdateForm(ModelForm):
    """
    Форма для смены данных профиля пользователя
    """
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['address'].required = True
        self.fields['phone'].required = True
        self.fields['city'].required = True
        self.fields['photo'] = ImageField(required=False, label='Аватар', widget=FileInput)

    class Meta:
        model = Profile
        fields = ("address", "phone", "city", "photo")

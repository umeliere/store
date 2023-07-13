from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, FileInput, ImageField

from core import settings
from users.models import Profile


class UserRegisterForm(UserCreationForm):
    """
    Форма для регистрации пользователя
    """
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='ReCAPTCHA')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", 'password1', 'password2', 'recaptcha')


class UserLoginForm(AuthenticationForm):
    """
    Форма авторизации на сайте
    """
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='ReCAPTCHA')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", 'password', 'recaptcha')


class ProfileUpdateForm(ModelForm):
    """
    Форма для смены данных профиля пользователя
    """
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='ReCAPTCHA')

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['photo'] = ImageField(required=False, label='Аватар', widget=FileInput)

    class Meta:
        model = Profile
        fields = ("address", "phone", "city", "photo")

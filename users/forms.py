from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, FileInput, ImageField

from core import settings
from users.models import Profile


class UserRegisterForm(UserCreationForm):
    """
    Sign up form
    """
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='ReCAPTCHA')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    def clean_email(self):
        """
        Check the email for uniqueness
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError('Такой email уже используется')
        return email

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", 'password1', 'password2', 'recaptcha')


class UserLoginForm(AuthenticationForm):
    """
    Log in form
    """
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='ReCAPTCHA')

    class Meta:
        model = User
        fields = ("username", 'password', 'recaptcha')


class UserPasswordChangeForm(PasswordChangeForm):
    """
    Change the password form
    """
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='ReCAPTCHA')

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2', 'recaptcha')


class UserForgotPasswordForm(PasswordResetForm):
    """
    Reset the password form
    """
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='ReCAPTCHA')

    class Meta:
        model = User
        fields = ('email', 'recaptcha')


class UserSetNewPasswordForm(SetPasswordForm):
    """
    Reset the password after the confirmation form
    """
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='ReCAPTCHA')

    class Meta:
        model = User
        fields = ('user', 'new_password1', 'new_password2', 'recaptcha')


class ProfileUpdateForm(ModelForm):
    """
    The user profile update form
    """
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='ReCAPTCHA')

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['photo'] = ImageField(required=False, label='Аватар', widget=FileInput)

    class Meta:
        model = Profile
        fields = ("address", "phone", "city", "photo", 'recaptcha')

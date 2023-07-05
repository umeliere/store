from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from users.models import Profile

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class ProfileForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "address", "phone", "city")

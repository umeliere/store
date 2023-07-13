from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView

from users.forms import (
    UserRegisterForm,
    UserLoginForm,
    ProfileUpdateForm,
    UserPasswordChangeForm,
    UserForgotPasswordForm,
    UserSetNewPasswordForm,
)
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from users.models import Profile


class SignUpView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации пользователя
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'
    success_message = 'Вы успешно зарегистрировались.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Зарегистрироваться'
        return context


class MyLoginView(SuccessMessageMixin, LoginView):
    """
    Представление входа пользователя
    """
    form_class = UserLoginForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('store:discount_page')
    success_message = 'Вы успешно вошли.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context


class UserPasswordChangeView(PasswordChangeView):
    """
    Изменение пароля пользователя
    """
    form_class = UserPasswordChangeForm
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy("password_change_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля на сайте'
        return context


class UserPasswordResetView(PasswordResetView):
    """
    Сброс пароля пользователя
    """
    form_class = UserForgotPasswordForm
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy("password_reset_done")
    subject_template_name = 'registration/password_reset_subject.txt'
    email_template_name = 'registration/password_reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сброс пароля'
        return context


class UserPasswordSetView(PasswordResetConfirmView):
    """
    Установление нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy("password_reset_complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установление нового пароля'
        return context


class ProfilePageView(LoginRequiredMixin, DetailView):
    """
    Представление профиля пользователя
    """
    queryset = Profile.objects.select_related('user')
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя {self.object.user.username}'
        return context


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление обновление профиля пользователя
    """
    model = Profile
    queryset = Profile.objects.select_related('user')
    template_name = 'users/update_profile.html'
    form_class = ProfileUpdateForm
    success_message = 'Вы успешно изменили данные'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление страницы'
        if self.request.POST:
            context['profile_form'] = ProfileUpdateForm(self.request.POST, instance=self.request.user.profile)
        else:
            context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']
        profile_form.save()
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'slug': self.object.slug})

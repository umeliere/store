from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import DetailView

from users.forms import UserForm, ProfileUpdateForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages

from users.models import Profile


class SignUpView(CreateView):
    """
    Представление регистрации пользователя
    """
    form_class = UserForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Зарегистрироваться'
        return context


class MyLoginView(LoginView):
    """
    Представление входа пользователя
    """
    template_name = 'users/login.html'
    next_page = reverse_lazy('store:discount_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


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


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление обновление профиля пользователя
    """
    model = Profile
    queryset = Profile.objects.select_related('user')
    template_name = 'users/update_profile.html'
    form_class = ProfileUpdateForm

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

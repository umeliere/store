from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from users.forms import UserForm, ProfileForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages

from users.models import Profile


class SignUpView(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


class MyLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('store:discount_page')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class ProfilePageView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('users:login')
    queryset = Profile.objects.select_related('user')
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя {self.object.user.username}'
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    login_url = reverse_lazy('users:login')
    queryset = Profile.objects.select_related('user')
    template_name = 'users/update_profile.html'
    form_class = ProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление страницы'
        if self.request.POST:
            context['profile_form'] = ProfileForm(self.request.POST, instance=self.request.user.profile)
        else:
            context['profile_form'] = ProfileForm(instance=self.request.user.profile)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']
        profile_form.save()
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'slug': self.object.slug})

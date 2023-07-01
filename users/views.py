from django.contrib.auth.views import LoginView, LogoutView

from users import forms
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages


class SignUpView(generic.CreateView):
    form_class = forms.CreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


class MyLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('store:discount_page')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

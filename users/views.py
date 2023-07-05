from django.contrib.auth.views import LoginView, LogoutView

from users.forms import CreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages


class SignUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


class MyLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('store:discount_page')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

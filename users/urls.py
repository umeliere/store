from django.urls import path
from users.views import SignUpView, MyLoginView, LogoutView, ProfilePageView, ProfileUpdateView

app_name = 'users'
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='store:discount_page'), name='logout'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='update_profile'),
    path('profile/<str:slug>/', ProfilePageView.as_view(), name='profile'),
]

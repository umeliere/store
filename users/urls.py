from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
)
from django.urls import path
from users.views import SignUpView, MyLoginView, LogoutView, ProfilePageView, ProfileUpdateView

app_name = 'users'
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='store:discount_page'), name='logout'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='update_profile'),
    path('profile/<str:slug>/', ProfilePageView.as_view(), name='profile'),
    # представления смены пароля
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    # представления сброса пароля
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

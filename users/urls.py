from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)
from django.urls import path
from users.views import (
    SignUpView,
    MyLoginView,
    LogoutView,
    ProfilePageView,
    ProfileUpdateView,
    UserPasswordChangeView,
    UserPasswordResetView,
    UserPasswordSetView,
)

app_name = 'users'
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='store:discount_page'), name='logout'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='update_profile'),
    path('profile/<str:slug>/', ProfilePageView.as_view(), name='profile'),
    # change the password views
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    # reset the password views
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserPasswordSetView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

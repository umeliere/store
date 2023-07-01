from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='store:discount_page'), name='logout'),
]

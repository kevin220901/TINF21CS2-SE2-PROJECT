from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, ChangePasswordView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password')
]

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('sign_up/', views.registration_view, name='sign_up'),

    path('verify_email/<uidb64>/<token>/', views.verify_email, name='verify_email'),

    path('resend_verification_email/', views.resend_verification_email, name='resend_verification_email'),

    path('sign_in/', views.login_view, name='sign_in'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

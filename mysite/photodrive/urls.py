from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path("home/", views.main_menu, name="menu"),
    path('register/', views.registerPage, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name='registration/logout.html'), name="logout"),
    path("upload/", views.uploadPage, name="upload"),
    path("gallery/", views.viewPhoto, name="gallery"),
    path("gallery/<slug>/", views.deletePhotoView, name='delete'),
    path("delete-photo/<slug>/", views.delete_photo, name='delete-photo'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
]

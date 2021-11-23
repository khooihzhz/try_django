from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView
from .models import *
from .forms import UserForm, PhotoForm, CaptchaAuthenticationForm


def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("menu")
    return render(request, "content/home.html")


class DeletePhotoView(LoginRequiredMixin, DetailView):
    model = Photo
    login_url = '/login'
    template_name = 'content/delete_photo.html'


@login_required(login_url='/login')
def deletePhotoView(request, slug):
    image = get_object_or_404(Photo, slug=slug)
    if request.user != image.user:
        messages.info(request, 'nice try ')
        return redirect('gallery')
    context = {
        'object': image
    }
    return render(request=request, template_name='content/delete_photo.html', context=context)


@login_required(login_url='/login')
def main_menu(request):
    return render(request, "content/menu.html")


@login_required(login_url='/login')
def uploadPage(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            photo = form.save(commit=False)
            photo.user = user
            photo.save()
            messages.success(request, 'Photo Added')
            return redirect('upload')

    form = PhotoForm   # return an empty form
    return render(request=request, template_name='content/add_photo.html', context={'form': form})


def delete_photo(request, slug):
    image = get_object_or_404(Photo, slug=slug)
    image.delete()
    messages.info(request, "photo deleted")
    return redirect('gallery')


@login_required(login_url='/login')
def viewPhoto(request):
    try:
        user_photo = Photo.objects.filter(user=request.user)
        context = {
            'gallery': user_photo
        }
        return render(request, 'content/view_photo.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "No Photo Yet, add some photo")
        return redirect('upload')


def login_request(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("menu")
    if request.method == "POST":
        form = CaptchaAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("menu")
        else:
            messages.error(request, 'Invalid Information, Try Again!')
            return redirect('login')
    form = CaptchaAuthenticationForm
    return render(request=request, template_name="registration/login.html", context={"login_form": form})


def registerPage(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("menu")
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account Created, redirecting to Login Page")
            return redirect('login')
        else:
            messages.error(request, "Register unsuccessful, Invalid Information.")
    form = UserForm
    return render(request=request, template_name="registration/register.html", context={"register_form": form})


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})

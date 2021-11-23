from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from datetime import datetime


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    f = open("user.log", "a")
    f.write('{} : user {} logged in \n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user.username))
    f.close()


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    f = open("user.log", "a")
    f.write('{} user {} failed to login\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), credentials["username"]))
    f.close()


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    f = open("user.log", "a")
    f.write('{} user {} logged out\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user.username))
    f.close()
from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from autoslug.settings import slugify as default_slugify
from django.urls import reverse


def custom_slugify(value):
    value = value.lower()
    return default_slugify(value).replace('-', '_')


# Create your models here.
class Photo(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(null=True, blank=True, upload_to="images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_date = models.DateField(auto_now_add=True)
    slug = AutoSlugField(populate_from='name', unique=True, slugify=custom_slugify, null=True)

    def __str__(self):
        return f"{self.slug}"

    def get_absolute_url(self):
        return reverse("delete", kwargs={
            'slug': self.slug
        })

    def get_remove_photo_url(self):
        return reverse("delete-photo", kwargs={
            'slug': self.slug
        })



from django_countries.fields import CountryField
from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField
from django_resized import ResizedImageField


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = CountryField(blank_label='(Select country)', blank=True)
    linked_in = models.CharField(max_length=255, blank=True)
    facebook = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    github = models.CharField(max_length=255, blank=True)
    objective = HTMLField(blank=True)
    profile_pic = ResizedImageField(size=[300, 300], quality=100, default="profile-pics/default.jpg", upload_to="profile-pics")
    sub_expires_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.email


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    package = models.CharField(max_length=255)
    total = models.IntegerField()
    paid_status = models.BooleanField(default=False)

    def __str__(self):
        return self.package

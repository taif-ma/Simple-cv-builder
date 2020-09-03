from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User, Profile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', ]


class ProfileAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'address',
        'city',
        'country',
        'phone_number',
        'objective',
        'linked_in',
        'profile_pic',
        'sub_expires_on',
    )





admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)

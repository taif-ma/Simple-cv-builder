from django import forms
from django.forms import TextInput
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django.contrib.auth.password_validation import validate_password


class CustomUserCreationForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 8:
            raise forms.ValidationError("Your username is too short. A username must be at least 8 characters long")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Your username is already taken")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if validate_password(password1):
            raise forms.ValidationError('This password is not valid')
        return password1

    def clean(self, *args, **kwargs):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match. Please try again")
        return super(UserCreationForm, self).clean(*args, **kwargs)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', )
        widgets = {'first_name': TextInput(attrs={'placeholder': 'What is your first name?'}),
                   'last_name': TextInput(attrs={'placeholder': 'What is your last name?'}), }


class OrderForm(forms.Form):
    pass


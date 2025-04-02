from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.forms import PasswordInput
from users.models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            raise ValidationError("Email yoki parol noto‘g‘ri!")

        user = authenticate(self.request, email=email, password=password)
        if user is None:
            raise ValidationError("Email yoki parol noto‘g‘ri!")

        return cleaned_data



class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'confirm_password')

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'{email} emaili allaqachon ro‘yxatdan o‘tgan!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Parollar mos kelmadi!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Parolni hash qilish
        if commit:
            user.save()
        return user

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if password != confirm_password:
            raise forms.ValidationError(f'Password don\'t match')
        return confirm_password

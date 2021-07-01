from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from authapp.models import User


class UserLoginForm(AuthenticationForm):
    """Форма для аутентификации"""

    class Meta:
        model = User
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации"""
    Captcha = CaptchaField()

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name',
            'email', 'birth_date', 'gender',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_email(self):
        email_user = self.cleaned_data['email']
        email_data = User.objects.filter(email=email_user)
        if email_data:
            raise forms.ValidationError(
                'Пользователь с таким email уже зарегистрирован'
            )
        return email_user

import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, \
    UserChangeForm, UsernameField
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CustomUserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    A custom form for registering a new user.
    """

    phone = forms.CharField(
        max_length=12,
        label='Phone number',
        help_text='Enter your phone number',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number'}),
    )

    password1 = forms.CharField(
        label='Password',
        help_text='Enter your password',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )

    password2 = forms.CharField(
        label='Confirm password',
        help_text='Enter your password again',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
    )

    class Meta:
        model = User
        fields = ('phone', 'password1', 'password2')

    def clean_phone(self):
        """
        A method to clean and validate the phone number field.

        Parameters:
            self: the instance of the form
        Returns:
            phone: the cleaned and validated phone number
        """
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Phone number already exists')
        elif not re.match(r'^\+7\d{10}$', phone):
            raise forms.ValidationError('Phone number must start with +7 and contain 10 digits')
        return phone

    def save(self, commit=True):
        """
        Save the user data with an option to immediately commit the changes to the database.

        :param commit: A boolean indicating whether to commit the changes to the database immediately. Default is True.
        :return: The user object after saving the data.
        """
        user = super().save(commit=False)
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(StyleFormMixin, AuthenticationForm):
    """
    A custom form for authenticating a user.
    """
    username = forms.CharField(
        max_length=12,
        label='Phone number',
        help_text='Enter your phone number',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number'}),
    )

    password = forms.CharField(
        label='Password',
        help_text='Enter your password',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )

    class Meta:
        model = User
        fields = ('phone', 'password')


class CustomUserChangeForm(StyleFormMixin, UserChangeForm):
    """
    A custom form for changing user data.
    """

    class Meta:
        model = User
        fields = ('phone', 'avatar')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    email = forms.EmailField(
        required=False,
        widget=forms.HiddenInput(),
    )
    phone = forms.CharField(
        max_length=12,
        label='Phone number',
        help_text='Enter your phone number',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number'}),
    )

    class Meta:
        model = User
        fields = ('phone',)

    def clean_phone(self):
        """
        A method to clean and validate the phone number field.

        Parameters:
            self: the instance of the form
        Returns:
            phone: the cleaned and validated phone number
        """
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+7\d{10}$', phone):
            raise forms.ValidationError('Phone number must start with +7 and contain 10 digits')
        return phone

    def save(self, request, **kwargs):
        """
        Save the user data based on the provided phone number.

        :param request: The request object containing user data.
        :param kwargs: Additional keyword arguments.
        :return: A tuple containing the token and uid generated.
        """
        phone = self.cleaned_data['phone']
        user = User.objects.get(phone=phone)
        token_generator = kwargs.get('token_generator', default_token_generator)
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        return token, uid


class CustomResetConfirmForm(StyleFormMixin, SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password',
        help_text='Enter your new password',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}),
    )

    new_password2 = forms.CharField(
        label='Confirm new password',
        help_text='Enter your new password again',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
    )

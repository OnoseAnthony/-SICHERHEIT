from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from manager.models import User
from manager.password_generator import register_passphrase as get_passphrase



#create your forms here

class RegisterForm(UserCreationForm):


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username')


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        cleaned_username = self.cleaned_data.get('username')
        cleaned_email_address = self.cleaned_data.get('email')
        cleaned_password = self.cleaned_data.get('password1')
        user.login_passphrase = get_passphrase(cleaned_username, cleaned_email_address, 15)
        user.save()

        return user



class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users/secretaries. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email', 'username', 'login_passphrase'
             )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password1 = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email','username',
             )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password1"]

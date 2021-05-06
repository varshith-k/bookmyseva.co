from django import forms
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'fullname','mobile_number','address','city','main_service')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin','fullname','mobile_number','address','city','main_service')

    def clean_password(self):
        return self.initial["password"]

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','fullname','mobile_number','address','city','main_service')

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    fullname = forms.CharField(max_length=50)
    mobile_number = forms.IntegerField()
    address = forms.CharField(max_length=500)
    city = forms.CharField(max_length=50)
    main_service = forms.CharField(max_length=15)
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2','fullname','mobile_number','address','city','main_service']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name' , 'last_name' , 'username' , 'email' )

from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu cũ'}))
    new_password1 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu mới'}))
    new_password2 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập lại mật khẩu mới'}))

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = False
        self.fields['new_password1'].label = False
        self.fields['new_password2'].label = False
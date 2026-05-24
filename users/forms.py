from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class ProfileEditForm(forms.ModelForm):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'style': 'background: #222; color: white; padding: 8px; border: 1px solid #555; width: 100%; box-sizing: border-box;'
        }),
        label="Поточний пароль для підтвердження змін"
    )

    class Meta:
        model = CustomUser
        
        fields = ('username', 'email', 'phone_number', 'avatar')
        widgets = {
            'username': forms.TextInput(attrs={'style': 'background: #222; color: white; padding: 8px; border: 1px solid #555; width: 100%; box-sizing: border-box;'}),
            'email': forms.EmailInput(attrs={'style': 'background: #222; color: white; padding: 8px; border: 1px solid #555; width: 100%; box-sizing: border-box;'}),
            'phone_number': forms.TextInput(attrs={'style': 'background: #222; color: white; padding: 8px; border: 1px solid #555; width: 100%; box-sizing: border-box;'}),
            'avatar': forms.FileInput(attrs={'style': 'color: white;'}),
        }

    def __init__(self, *args, **kwargs):
        # Передаємо поточного користувача у форму для перевірки пароля
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')

        if self.user and not self.user.check_password(current_password):
            raise forms.ValidationError("Невірний поточний пароль. Зміни не збережено!")
        return current_password
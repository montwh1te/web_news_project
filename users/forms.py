from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuarios

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário'}),
        label="Nome de Usuário",
        min_length=5,
        help_text="O nome de usuário deve ter pelo menos 5 caracteres."
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}),
        label="E-mail"
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
        label="Senha",
        min_length=10,
        help_text="A senha deve ter pelo menos 10 caracteres."
    )
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Senha'}),
        label="Confirmar Senha"
    )
    foto = forms.ImageField(
        widget=forms.FileInput(attrs={'placeholder': 'Foto de Perfil'}),
        label="Foto de Perfil",
        required=False
    )

    class Meta:
        model = Usuarios
        fields = ['username', 'email', 'senha', 'foto']
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'foto': 'Foto de Perfil'
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if senha != confirmar_senha:
            raise forms.ValidationError("As senhas não correspondem.")

        if len(senha) < 10:
            raise forms.ValidationError("A senha deve ter pelo menos 10 caracteres.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["senha"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário'}),
        label="Nome de Usuário"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
        label="Senha"
    )

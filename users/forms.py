from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuarios

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Primeiro nome'}),
        label="Primeiro Nome",
        min_length=1,
        help_text="O primeiro nome não deve conter caracteres especiais"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Sobrenome'}),
        label="Sobrenome",
        min_length=2,
        help_text="O sobrenome não deve conter caracteres especiais"
    )
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
        fields = ['first_name','last_name','username', 'email', 'senha', 'foto']
        labels = {
            'first_name': 'Primeiro Nome',
            'last_name': 'Sobrenome',
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'password': 'Senha',
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
    
class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['first_name', 'last_name', 'email', 'password', 'foto']
        widgets = {
            'senha': forms.PasswordInput(),
        }

class AlterarSenhaForm(forms.Form):
    senha_atual = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Senha Atual",
        required=True
    )
    senha_nova = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Nova Senha",
        required=True
    )
    confirmar_senha_nova = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmar Nova Senha",
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        senha_nova = cleaned_data.get("senha_nova")
        confirmar_senha_nova = cleaned_data.get("confirmar_senha_nova")

        if senha_nova and confirmar_senha_nova and senha_nova != confirmar_senha_nova:
            raise forms.ValidationError("As novas senhas não coincidem.")

        return cleaned_data
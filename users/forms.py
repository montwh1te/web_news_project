from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuarios
from django.core.exceptions import ValidationError
        
def validate_name(value):
    if not all(letra.isalpha() or letra == ' ' for letra in value):
        raise ValidationError(f'O nome deve ser composto apenas por letras e espaços.')

def validate_last_name(value):
    if not all(letra.isalpha() or letra == ' ' for letra in value):
        raise ValidationError(f'O sobrenome deve ser composto apenas por letras e espaços.')
        
class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Primeiro nome'}),
        label="Primeiro Nome",
        strip=True,
        min_length=2,
        validators=[validate_name],
        error_messages={
        'required': 'Este campo é obrigatório.',
        'min_length': 'O nome deve ter pelo menos 2 caracteres.',
        'validators': 'O nome deve conter apenas letras.',
    },
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Sobrenome'}),
        label="Sobrenome",
        strip=True,
        required=True,
        min_length=2,
        validators=[validate_last_name],
        error_messages={
        'required': 'Este campo é obrigatório.',
        'min_length': 'O sobrenome deve ter pelo menos 2 caracteres.',
        'validators': 'O sobrenome deve conter apenas letras.',
    },
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário'}),
        label="Nome de Usuário",
        strip=True,
        required=True,
        max_length=15,
        min_length=3,
        error_messages={
        'required': 'Este campo é obrigatório.',
        'min_length': 'O nome de usuário deve ter entre 3 e 15 caracteres.',
    },
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}),
        label="E-mail",
        required=True,
        error_messages={
        'required': 'Este campo é obrigatório.',
    },
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
        label="Senha",
        strip=True,
        required=True,
        min_length=7,
        error_messages={
        'required': 'Este campo é obrigatório.',
        'min_length': 'A senha deve ter possuir mais de 7 caracteres.',
    },
    )
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Senha'}),
        label="Confirmar Senha",
        strip=True,
        required=True,
        error_messages={
        'required': 'Este campo é obrigatório.',
    },
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
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuarios.objects.filter(username__iexact=username).exists():
            raise ValidationError("Já existe um usuário com esse nome de usuário.")
        return username    

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if senha and confirmar_senha and senha != confirmar_senha:
            raise ValidationError({
                "confirmar_senha": "As senhas não correspondem."
            })

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["senha"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário'}),
        label="Nome de Usuário",
        strip=True,
        required=True,
        error_messages={
        'required': 'Este campo é obrigatório.',
    },
        
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
        label="Senha",
        strip=True,
        required=True,
        error_messages={
        'required': 'Este campo é obrigatório.',
    },
    )
    
class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['first_name', 'last_name', 'username', 'email', 'foto']
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
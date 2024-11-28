from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuarios
from django.core.exceptions import ValidationError   
from django.contrib.auth import authenticate
          
class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Primeiro nome'}),
        label=None,  # Remove a label
        strip=True,
        min_length=2,
        error_messages={
            'required': 'Este campo é obrigatório.',
            'min_length': 'O nome deve ter pelo menos 2 caracteres.',
        },
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Sobrenome'}),
        label=None,  # Remove a label
        strip=True,
        required=True,
        min_length=2,
        error_messages={
            'required': 'Este campo é obrigatório.',
            'min_length': 'O sobrenome deve ter pelo menos 2 caracteres.',
        },
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário'}),
        label=None,  # Remove a label
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
        label=None,  # Remove a label
        required=True,
        error_messages={
            'required': 'Este campo é obrigatório.',
        },
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
        label=None,  # Remove a label
        strip=True,
        required=True,
        min_length=7,
        error_messages={
            'required': 'Este campo é obrigatório.',
            'min_length': 'A senha deve possuir no mínimo 7 caracteres.',
        },
    )
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Senha'}),
        label=None,  # Remove a label
        strip=True,
        required=True,
        error_messages={
            'required': 'Este campo é obrigatório.',
        },
    )
    foto = forms.ImageField(
        widget=forms.FileInput(attrs={'placeholder': 'Foto de Perfil'}),
        label=None,  # Remove a label
        required=False
    )
    is_staff = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    is_superuser = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
            'foto': 'Foto de Perfil',
        }

    # Sobrescrevendo o __init__ para aceitar o parâmetro 'user'
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Verifica se o usuário é superusuário
        if user and not user.is_superuser:
            # Remove os campos is_staff e is_superuser se não for superusuário
            self.fields.pop('is_staff')
            self.fields.pop('is_superuser')



        
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not all(letra.isalpha() or letra == ' ' for letra in first_name):
            raise ValidationError("O nome deve ser composto apenas por letras e espaços.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not all(letra.isalpha() or letra == ' ' for letra in last_name):
            raise ValidationError("O sobrenome deve ser composto apenas por letras e espaços.")
        return last_name
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuarios.objects.filter(username__iexact=username).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return username 
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        dominios_permitidos = ["@gmail.com","@outlook.com","@hotmail.com","@live.com","@msn.com","@yahoo.com","@ymail.com","@rocketmail.com","@icloud.com","@me.com","@mac.com","@proton.me","@protonmail.com","@zoho.com","@uol.com.br", "@terra.com.br", "@bol.com.br", "@globo.com", "@ig.com.br", "@r7.com", "@zipmail.com.br", "@oi.com.br"]
        if not any(email.endswith(dominio) for dominio in dominios_permitidos):
            raise ValidationError("O e-mail deve pertencer a um dos domínios permitidos.")
        if Usuarios.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email
       
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

        # A senha já está sendo tratada no formulário, mas precisamos garantir que ela seja salva de forma segura
        senha = self.cleaned_data["senha"]
        user.set_password(senha)  # Use o método set_password para salvar a senha de forma segura

        user.first_name = self.cleaned_data["first_name"].title()  # Padroniza o nome
        user.last_name = self.cleaned_data["last_name"].title()    # Padroniza o sobrenome

        # Verifica se é superusuário ou staff
        if self.cleaned_data.get("is_superuser"):
            user.is_superuser = True
            user.is_staff = True  # Superusuários geralmente são também staff
        elif self.cleaned_data.get("is_staff"):
            user.is_staff = True

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
    
    def clean(self):
            # Chama a validação padrão do formulário
            cleaned_data = super().clean()

            # Recupera os dados de username e password
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')

            # Autentica o usuário
            user = authenticate(username=username, password=password)
            if user is None:
                # Se a autenticação falhar, adiciona um erro geral
                raise ValidationError("Nome de usuário ou senha inválidos.")

            # Retorna os dados limpos se não houver problemas
            return cleaned_data





class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['first_name', 'last_name', 'username', 'email', 'foto']
        widgets = {
            'senha': forms.PasswordInput(),
        }
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        dominios_permitidos = ["@gmail.com","@outlook.com","@hotmail.com","@live.com","@msn.com","@yahoo.com","@ymail.com","@rocketmail.com","@icloud.com","@me.com","@mac.com","@proton.me","@protonmail.com","@zoho.com","@uol.com.br", "@terra.com.br", "@bol.com.br", "@globo.com", "@ig.com.br", "@r7.com", "@zipmail.com.br", "@oi.com.br"]
        if not any(email.endswith(dominio) for dominio in dominios_permitidos):
            raise forms.ValidationError("O e-mail colocado anteriormente deve pertencer a um dos domínios permitidos.")
        if Usuarios.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("O email colocado anteriormente já encontra-se em uso.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuarios.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("O usuário colocado anteriormente já encontra-se em uso.")
        if len(username) < 3 or len(username) > 15:
            raise forms.ValidationError("O nome de usuário colocado anteriormente deve possuir entre 3 e 15 caracteres.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 2:
            raise forms.ValidationError("O nome deve ter pelo menos 2 caracteres.")
        if not all(letra.isalpha() or letra == ' ' for letra in first_name):
            raise forms.ValidationError(f'O nome deve ser composto apenas por letras e espaços.')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) < 2:
            raise forms.ValidationError("O sobrenome deve ter pelo menos 2 caracteres.")
        if not all(letra.isalpha() or letra == ' ' for letra in last_name):
            raise forms.ValidationError(f'O sobrenome deve ser composto apenas por letras e espaços.')
        return last_name
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"].title() # Padroniza o nome
        user.last_name = self.cleaned_data["last_name"].title() # Padroniza o sobrenome
        if commit:
            user.save()
        return user 

class AlterarSenhaForm(forms.Form):
    senha_atual = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Senha Atual",
        required=True
    )
    senha_nova = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Nova senha'}),
        label="Nova Senha",
        strip=True,
        required=True,
        min_length=7,
        error_messages={
        'required': 'Este campo é obrigatório.',
        'min_length': 'A senha deve possuir no mínimo 7 caracteres.',
    },
    )
    confirmar_senha_nova = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar nova senha'}),
        label="Confirmar Nova Senha",
        strip=True,
        required=True,
        error_messages={
        'required': 'Este campo é obrigatório.',
    },
    )

    def clean(self):
        cleaned_data = super().clean()
        senha_nova = cleaned_data.get("senha_nova")
        confirmar_senha_nova = cleaned_data.get("confirmar_senha_nova")

        if len(senha_nova) < 7 or len(confirmar_senha_nova) < 7:
            raise ValidationError("A senha deve possuir no mínimo 7 caracteres.")

        if senha_nova and confirmar_senha_nova and senha_nova != confirmar_senha_nova:
            raise ValidationError("As novas senhas não coincidem.")

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["senha"]) # Transforma a senha em SHAHash
        if commit:
            user.save()
        return user
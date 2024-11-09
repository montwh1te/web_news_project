from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Usuarios
from .forms import RegistrationForm, LoginForm 

# Função da página inicial
def home(request):
    return render(request, 'index.html')

# Função de registro (consolidada para evitar duplicação)
def registro(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)  # Incluindo request.FILES para upload de imagem
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['senha'])  # Define a senha corretamente
            user.save()
            login(request, user)  # Login automático após o registro
            return redirect('home')  # Redireciona para a página inicial após o registro
    else:
        form = RegistrationForm()
    return render(request, 'registro.html', {'form': form})

# Função de login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Nome de usuário ou senha inválidos.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Função de logout
def logout_view(request):
    logout(request)
    return redirect('home')

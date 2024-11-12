from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm


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
    return render(request, 'registro', {'form': form})


# Função de login
def login(request):
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
def logout(request):
    logout(request)
    return redirect('home')
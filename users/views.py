from django.contrib.auth import logout, login as auth_login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm

def registro(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['senha'])
            user.save()
            auth_login(request, user)  # Usa a função de login do Django com o alias 'auth_login'
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, "users/registro.html", {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Usa a função de login do Django com o alias 'auth_login'
                return redirect('home')
            else:
                form.add_error(None, "Nome de usuário ou senha inválidos.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
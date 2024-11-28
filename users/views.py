from django.contrib.auth import logout, login as auth_login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, UsuarioUpdateForm, AlterarSenhaForm
from .models import Usuarios
from django.http import JsonResponse
from trendfeeds.models import Categoria, TimeFavorito


def login_view(request):
    form_login = LoginForm()
    form_register = RegistrationForm(user=request.user)

    if request.method == 'POST':
        if 'login' in request.POST:
            form_login = LoginForm(request, data=request.POST)
            if form_login.is_valid():
                # Se `is_valid` passar, o usuário já foi autenticado
                user = form_login.get_user()
                auth_login(request, user)  # Faz o login do usuário
                if user.is_superuser:
                    return redirect('pagina_funcionarios')
                return redirect('home')
            else:
                print("Erros do formulário de login:", form_login.errors)

        elif 'register' in request.POST:
            form_register = RegistrationForm(request.POST, request.FILES, user=request.user)
            if form_register.is_valid():
                user = form_register.save()
                auth_login(request, user)
                return redirect('time_favorito')

    return render(request, 'users/login.html', {
        'form_login': form_login,
        'form_register': form_register
    })







def logout_view(request):
    logout(request)
    return redirect('home')

def info_perfil(request, perfil_id):
    user = Usuarios.objects.get(id = perfil_id)  # Recupera o usuário com o id do perfil
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()  # Salva os dados atualizados no banco
            return redirect('home')  # Redireciona para o perfil atualizado
    else:
        form = UsuarioUpdateForm(instance=user)  # Preenche o formulário com os dados do usuário

    context = {'user': user, 'form': form}
    return render(request, 'users/perfil.html', context)

def alterar_senha(request):
    if request.method == "POST":
        form = AlterarSenhaForm(request.POST)
        if form.is_valid():
            senha_atual = form.cleaned_data['senha_atual']
            senha_nova = form.cleaned_data['senha_nova']

            # Verificar se a senha atual está correta
            user = authenticate(username=request.user.username, password=senha_atual)
            if user is not None:
                # Alterar para a nova senha
                user.set_password(senha_nova)
                user.save()
                
                # Deslogar o usuário para que ele faça login com a nova senha
                logout(request)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Senha atual incorreta'})
            
        # Se o formulário não for válido, retornar os erros
        return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False})

def time_favorito(request):
    # Pega todos os times disponíveis na tabela Categoria
    categorias = Categoria.objects.all()

    if request.method == "POST":
        # Pega o time favorito escolhido pelo usuário
        categoria_id = request.POST.get("categoria")
        categoria = Categoria.objects.get(id=categoria_id)
        
        # Verifica se o usuário já tem um time favorito
        time_favorito, created = TimeFavorito.objects.get_or_create(usuario=request.user)
        
        # Associa o time favorito à categoria escolhida
        time_favorito.categoria = categoria
        time_favorito.save()
        
        return redirect('home')

    # Contexto com todos os times
    context = {'categorias': categorias}
    return render(request, 'users/time_favorito.html', context)
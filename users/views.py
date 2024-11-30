from django.contrib.auth import logout, login as auth_login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, UsuarioUpdateForm, AlterarSenhaForm
from .models import Usuarios
from django.http import JsonResponse
from trendfeeds.models import Categoria, TimeFavorito
from django.contrib import messages
import requests
import http.client

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

def time_favorito(request, page="A"):
    # Pega todos os times disponíveis na tabela Categoria
    categorias = Categoria.objects.all()

    if request.method == "POST":
        
        descricao_ativa = request.POST.get('descricao_ativa')

        try:
            categoria = Categoria.objects.get(descricao=descricao_ativa)
        except Categoria.DoesNotExist:
            messages.error(request, "Nenhum time correspondente foi encontrado.")
            return redirect('time_favorito_default')
        
        
        # Verifica se o usuário já tem um time favorito para essa categoria
        existing_time_favorito = TimeFavorito.objects.filter(usuario=request.user, time=categoria).first()

        if existing_time_favorito:
            messages.info(request, "Você já escolheu este time como favorito.")
            return redirect('time_favorito_default') # Abrir pop-up na página
        
        
        # Verifica se o usuário já tem um time favorito
        existing_time = TimeFavorito.objects.filter(usuario=request.user).first()

        if existing_time:
            # Atualiza o time favorito existente
            existing_time.time = categoria
            existing_time.save()
            messages.success(request, f"Seu time favorito foi atualizado para {categoria.nome}!")
            return redirect('boas_vindas', time_fav=categoria.nome)

        # Criação do time favorito
        time_favorito, created = TimeFavorito.objects.get_or_create(usuario=request.user, time=categoria)

        # Redireciona para a página inicial ou outra página
        return redirect('boas_vindas', time_fav=categoria.nome)

    # Escolhe o template com base no parâmetro da URL
    template_name = f'users/time_favorito_{page}.html'

    # Contexto com todas as categorias
    context = {'categorias': categorias, 'page': page}
    return render(request, template_name, context)






def boas_vindas(request, time_fav):
    # Pega todos os times disponíveis na tabela Categoria
    categorias = Categoria.objects.all()

    try:
        time_captado = Categoria.objects.get(nome=time_fav)
    except Categoria.DoesNotExist:
        messages.error(request, "Nenhum time correspondente foi encontrado. Erro.")
        return redirect('home')

    # Chama a API externa para pegar informações sobre o time
    api_url = f"http://127.0.0.1:8000/api/times/{time_captado.time.id}/"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        api_local = response.json()
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Erro ao chamar a API: {e}")
        api_local = {} 
        
    print(api_local)

    # Contexto com todas as categorias e o time escolhido
    context = {'categorias': categorias, 'time_fav': time_captado.nome, 'time_form': time_captado.nome_categoria, 'time_obj':time_captado, 'api_local': api_local}
    
    # Renderiza o template de boas-vindas
    return render(request, 'users/boas_vindas.html', context)

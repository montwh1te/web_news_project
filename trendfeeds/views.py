from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Usuarios, Noticias
from .forms import RegistrationForm, LoginForm
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.utils.text import slugify


def home(request):
    ultima_noticia = Noticias.objects.all().order_by('-id').first()
    outras_noticias = Noticias.objects.all().order_by('-data_publicacao')[1:5]  # Outras notícias
    
    # Verificando se a última notícia e outras notícias possuem slug
    if ultima_noticia and not ultima_noticia.slug:
        ultima_noticia.slug = slugify(ultima_noticia.titulo)
        ultima_noticia.save()

    return render(request, 'html/index.html', {'ultima_noticia': ultima_noticia, 'outras_noticias': outras_noticias})

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


def detalhes_noticia(request, slug):
    noticia = get_object_or_404(Noticias, slug=slug)
    
    # Gerar o nome do template com base no slug
    template_name = f'html/noticias/{noticia.slug}.html'
    
    return render(request, template_name, {'noticia': noticia})
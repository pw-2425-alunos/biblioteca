from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Autor, Livro
from .forms import AutorForm, LivroForm
import requests

def index_view(request):
    context = {
        'autores': Autor.objects.all().order_by('nome'),
    }
    
    

    dados = requests.get("https://a22202078.pw.deisi.ulusofona.pt/api/bands", verify=False)

    bandas = dados.json()
    
    print(bandas[4].get('nome'))
    
    
    return render(request, "biblioteca/index.html", context)



def autor_view(request, autor_id):
    context = {
        'autor': Autor.objects.get(id=autor_id),
    }
    return render(request, "biblioteca/autor.html", context)



def livro_view(request, livro_id):
    context = {
        'livro': Livro.objects.get(id=livro_id),
    }
    return render(request, "biblioteca/livro.html", context)


def generos_view(request):
    context = {
        'generos': Livro.objects.values_list('genero', flat=True).distinct()
        }
    return render(request, "biblioteca/generos.html", context)


def genero_view(request, genero):
    context = {
        'genero': genero,
        'livros': Livro.objects.filter(genero=genero),
    }
    return render(request, "biblioteca/genero.html", context)

@login_required
def novo_autor_view(request):
    form = AutorForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('autores')
    
    context = {'form': form}
    return render(request, 'biblioteca/novo_autor.html', context)


    
@login_required
def edita_autor_view(request, autor_id):
    autor = Autor.objects.get(id=autor_id)
    
    if request.POST:
        form = AutorForm(request.POST or None, request.FILES, instance=autor)
        if form.is_valid():
            form.save()
            return redirect('autores')
    else:
        form = AutorForm(instance=autor)
        
    context = {'form': form, 'autor':autor}
    return render(request, 'biblioteca/edita_autor.html', context)
    
from django.contrib.auth.decorators import login_required

@login_required
def apaga_autor_view(request, autor_id):
    autor = Autor.objects.get(id=autor_id)
    autor.delete()
    return redirect('autores')


@login_required
def novo_livro_view(request, autor_id):
    autor = Autor.objects.get(id=autor_id)  # Retrieve the Autor object using autor_id
    form = LivroForm(request.POST or None, request.FILES)

    if form.is_valid():
        livro = form.save(commit=False)  # Create a Livro instance without saving to the database yet
        livro.autor = autor  # Set the autor attribute of the Livro instance
        livro.save()  # Save the Livro instance to the database
        return redirect('autores')
    
    context = {'form': form}
    return render(request, 'biblioteca/novo_livro.html', context)


def pesquisa_autor_view(request):
    context = {}
    
    if request.POST:
        pesquisa = request.POST['pesquisa']
        context['pesquisa'] = pesquisa
        context['autores'] = Autor.objects.filter(nome__contains=pesquisa)
    
    return render(request,"biblioteca/pesquisa-autor.html", context)



from django.contrib.auth import models, authenticate, login, logout

def registo_view(request):
    if request.method == "POST":
        models.User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            first_name=request.POST['nome'],
            last_name=request.POST['apelido'],
            password=request.POST['password']
        )
        return redirect('login')
        
    return render(request, 'biblioteca/registo.html')
   
   
def login_view(request):
    if request.method == "POST":
        
        # Verifica as credenciais
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            # Se as credenciais são válidas, faz login e redireciona
            login(request, user)
            return render(request, 'biblioteca/user.html')
        else:
            # Se inválidas, reenvia para login com mensagem
            render(request, 'biblioteca/login.html', {
                'mensagem':'Credenciais inválidas'
            })
        
    return render(request, 'biblioteca/login.html')

   
def logout_view(request):
    logout(request)
    return redirect('autores')


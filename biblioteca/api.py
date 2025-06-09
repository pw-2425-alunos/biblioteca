from ninja import NinjaAPI, Query
from .models import Autor, Livro
from .schemas import AutorIn, AutorOut, LivroIn, LivroOut, AutorOutComLivros, ErrorSchema
from typing import List, Optional
from django.shortcuts import get_object_or_404

api = NinjaAPI(
    title="API RESTful Biblioteca",
    description="API para gestão de biblioteca, com operações completas sobre os dados.",
    version="1.0.0",
    urls_namespace='biblioteca'
)


#### Autores

# listar autor
@api.get("autores/", 
         response={200: List[AutorOutComLivros]}, 
         tags=["Autores"], 
         description="Lista de autores e seus livros")
def lista_autores(request):
    return 200, Autor.objects.prefetch_related('livros')  
    # .prefetch_related() faz 2 queries apenas (autor e livros), 
    # em vez de N + 1 com .all()


# ver um autor
@api.get("autores/{autor_id}/", 
         response={200: AutorOutComLivros, 404: ErrorSchema}, 
         tags=["Autores"],
         description="Ver um autor e seus livros")
def ver_autor(request, autor_id):
    return 200, get_object_or_404(
        Autor.objects.prefetch_related("livros"), 
        id=autor_id
        )


# criar autor
@api.post("autores/", 
          response={201: AutorOut}, 
          tags=["Autores"],
          description="Cria um novo autor")
def cria_autor(request, data: AutorIn):
    return 201, Autor.objects.create(**data.dict())


# alterar autor
@api.put("autores/{autor_id}/",
         response={200: AutorOut, 404: ErrorSchema},
         tags=["Autores"],
         description="Atualiza autor")
def atualiza_autor(request, autor_id, data: AutorIn):
    autor = get_object_or_404(Autor, id=autor_id)
    for attr, value in data.dict().items():
        setattr(autor, attr, value)
    autor.save()
    return 200, autor


# apagar autor
@api.delete("autores/{autor_id}/", 
           response={204: None, 404: ErrorSchema}, 
           tags=["Autores"],
           description="Remove o autor")
def apaga_autor(request, autor_id: int):
    autor = get_object_or_404(Autor, id=autor_id)
    autor.delete()
    return 204, None


#### Livros

# listar livros
@api.get("livros/", 
         response={200: List[LivroOut]}, 
         tags=["Livros"],
         description="Lista todos os livros com informação de seu autor")
def lista_livros(request):
    return 200, Livro.objects.select_related("autor")


# ver um livro
@api.get("livros/{livro_id}/", 
         response={200: LivroOut, 404: ErrorSchema},
         tags=["Livros"],
         description="Ver um livro e seu autor")
def ver_livro(request, livro_id):
    return 200, get_object_or_404(
        Livro.objects.select_related("autor"), 
        id=livro_id
        )


# criar livro
@api.post("livros/", 
          response={201: LivroOut}, 
          tags=["Livros"],
          description="Cria um novo livro, com autor associado")
def cria_livro(request, data: LivroIn):
    autor_obj = get_object_or_404(Autor, id=data.autor)
    livro_data = data.dict(exclude={"autor"})
    livro = Livro.objects.create(**livro_data, autor=autor_obj)
    return 201, livro


# atualizar livro
@api.put("livros/{livro_id}/", 
         response={200: LivroOut, 404: ErrorSchema}, 
         tags=["Livros"],
         description="Atualiza livro")
def atualiza_livro(request, livro_id: int, data: LivroIn):
    livro = get_object_or_404(Livro, id=livro_id)
    for attr, value in data.dict().items():
        if attr == "autor":
            autor_obj = get_object_or_404(Autor, id=value)
            setattr(livro, "autor", autor_obj)
        else:
            setattr(livro, attr, value)
    livro.save()
    return 200, livro


# apagar livro
@api.delete("livros/{livro_id}/", 
           response={204: None, 404: ErrorSchema}, 
           tags=["Livros"],
           description="Remove o livro")
def apaga_livro(request, livro_id: int):
    livro = get_object_or_404(Livro, id=livro_id)
    livro.delete()
    return 204, None

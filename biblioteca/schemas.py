from ninja import Schema
from typing import List, Optional

# Schemas para Autor
class AutorIn(Schema):
    nome: str
    ano_nascimento: int
    nacionalidade: str
    retrato: Optional[str] = None # Tipo opcional: permite string ou None

class AutorOut(Schema):
    id: int
    nome: str
    ano_nascimento: int
    nacionalidade: str
    retrato: Optional[str] = None 
    

# Schemas para Livro
class LivroIn(Schema):
    titulo: str
    genero: str
    ano_publicacao: int
    excerto: Optional[str] = None
    autor: int

class LivroOut(Schema):
    id: int
    titulo: str
    genero: str
    ano_publicacao: int
    excerto: Optional[str] = None
    autor: AutorOut  
    
class AutorOutComLivros(AutorOut):
    livros: List[LivroOut]
    
class ErrorSchema(Schema):
    detail: str
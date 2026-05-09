from ninja import Schema
from typing import List, Optional

# Schemas para Autor
class AutorIn(Schema):
    nome: str
    ano_nascimento: int
    nacionalidade: str
    retrato: Optional[str] = None # Tipo opcional: permite string ou None

class AutorOut(AutorIn):
    id: int
    
# Schemas para Livro
class LivroIn(Schema):
    titulo: str
    genero: str
    ano_publicacao: int
    excerto: Optional[str] = None
    autor: int

class LivroOut(LivroIn):
    id: int
    autor: AutorOut  

class LivroOutSemAutor(Schema):
    id: int
    titulo: str
    genero: str
    ano_publicacao: int
    excerto: Optional[str] = None

class AutorOutComLivros(AutorOut):
    livros: List[LivroOutSemAutor]
    
class ErrorSchema(Schema):
    detail: str

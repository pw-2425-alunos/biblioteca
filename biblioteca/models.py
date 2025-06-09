from django.db import models

# Create your models here.

class Autor(models.Model):
    nome = models.CharField(max_length=50)
    ano_nascimento = models.IntegerField()
    nacionalidade = models.CharField(max_length=50)
    retrato = models.ImageField(upload_to="retratos", null=True, blank=True)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=50)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="livros")
    genero =  models.CharField(max_length=50)
    ano_publicacao = models.IntegerField()
    excerto = models.TextField(default='', null=True, blank=True)
    
    def __str__(self):
        return f"{self.titulo} ({self.autor})"

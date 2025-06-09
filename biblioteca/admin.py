from django.contrib import admin

# Register your models here.
from .models import *


class LivroAdmin(admin.ModelAdmin):
    ordering = ['autor', 'ano_publicacao']
    list_display = ['titulo', 'autor', 'ano_publicacao']
    list_filter = ['autor']

admin.site.register(Livro, LivroAdmin)


class LivroInline(admin.TabularInline):
    model = Livro

class AutorAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ['nome', 'ano_nascimento']
    list_editable = ['ano_nascimento']
    inlines = [LivroInline] # lista livros

admin.site.register(Autor, AutorAdmin)


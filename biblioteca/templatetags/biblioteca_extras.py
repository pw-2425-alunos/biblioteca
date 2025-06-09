# templatetags/inqueritos_extras.py
from django import template

register = template.Library()

@register.filter
def livros_ordenados(autor):
    return autor.livros.all().order_by('ano_publicacao')

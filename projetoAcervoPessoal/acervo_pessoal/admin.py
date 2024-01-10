from django.contrib import admin
from .models import Livro, Emprestimo, Contato, PesquisaItens
# Register your models here.
admin.site.register(Livro)
admin.site.register(Emprestimo)
admin.site.register(Contato)
admin.site.register(PesquisaItens)
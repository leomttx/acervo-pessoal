from django.db import models
from datetime import date

class Livro(models.Model):
    titulo = models.CharField(max_length=20)
    autor = models.CharField(max_length=25)
    data_publicacao = models.DateField(null=False)
    fotoCapa = models.ImageField(upload_to='livros_capas/', null=True, blank=True) #explicar
    qtd_total = models.PositiveIntegerField(default=0)
    livro_emprestado = models.BooleanField(default = False)

    def __str__(self):
        return "Livro #%d: %s" % (int(self.id), self.titulo)

#---------------------CONTATO-------------------------
class Contato(models.Model):
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    email = models.EmailField(null=False)

    def __str__(self):
        return self.nome

class Emprestimo(models.Model):

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('atrasado', 'Atrasado'),
        ('devolvido', 'Devolvido'),
    ]

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente') # explicar



    def __str__(self):
        return f"Empréstimo de {self.livro.titulo} para {self.contato.nome}"


#---------------------PESQUISA-------------------------
class PesquisaItens(models.Model):
    def pesquisa_por_nome(self, nome):
        return Livro.objects.filter(titulo__icontains=nome)

#---------------------DISPONIVEIS-------------------------
# class ListarItens_disponiveis(models.Model):
#     itens_disponiveis = models.ManyToManyField(Livro)

#     def adcionar_item_disponivel(self, livro):
#         if livro not in self.itens_disponiveis.all():
#             self.itens_disponiveis.add(livro)
#             return True
#         else:
#             return False

#     def remover_item_disponivel(self, livro):
#         if livro in self.itens_disponiveis.all():
#             self.itens_disponiveis.remove(livro)
#             return True
#         else:
#             return False

#     def listar_itens_emprestados(self):
#         return list(self.itens_emprestados.all())

# #---------------------EMPRESTADOS-------------------------

# class ListarItens_emprestados(models.Model):
#     itens_emprestados = models.ManyToManyField(Livro)

#     def adcionar_item_emprestado(self, livro):
#         if livro not in self.itens_emprestados.all():
#             self.itens_emprestados.add(livro)
#             return True
#         else:
#             return False

#     def remover_item_emprestado(self, livro):
#         if livro in self.itens_emprestados.all():
#             self.itens_emprestados.remove(livro)
#             return True
#         else:
#             return False

#     def listar_itens_emprestados(self):
#         return list(self.itens_emprestados.all())




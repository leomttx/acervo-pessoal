
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Livro, PesquisaItens, Contato
from .models import Emprestimo
from datetime import datetime
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required(login_url='/acervo_pessoal/login_usuario/')
def cad_livro(request):
    if request.method =='POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        data_publicacao = request.POST.get('data_publicacao')
        qtd_total = request.POST.get('qtd_total')
        fotoCapa = request.FILES.get('fotoCapa')



        Livro.objects.create(
            titulo = titulo,
            autor = autor,
            data_publicacao = data_publicacao,
            qtd_total = qtd_total,
            fotoCapa = fotoCapa,
        )

        return redirect(reverse('acervo_pessoal:lista_livros_disponiveis')) # Redireciona para a página de listagem de livros
    return render(request, 'acervo_pessoal/cad_livro.html')

#---------------------------------------------------------------------------------------------------------------

@login_required(login_url='/acervo_pessoal/login_usuario/')
def lista_livros_disponiveis(request):
    livros = Livro.objects.filter(livro_emprestado=False) #pega todos os objetos do Model Livro e armazena em livros
    return render(request, 'acervo_pessoal/lista_livros_disponiveis.html', {'livros':livros})

#---------------------------------------------------------------------------------------------------------------

def cad_usuario(request):
    if request.method == "GET":
        return render(request, 'acervo_pessoal/cad_usuario.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first() #...

        if user:
            return HttpResponse("Já existe um usuário com esse username")

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()


        return HttpResponse("Usuário cadastrado com sucesso!")

#---------------------------------------------------------------------------------------------------------------

def login_usuario(request):
    if request.method == "GET":
        return render(request, 'acervo_pessoal/login_usuario.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
            livros = Livro.objects.all()
            return redirect(reverse('acervo_pessoal:lista_livros_disponiveis'))
        else:
            return HttpResponse('Email ou senha Inavalidos')

#---------------------------------------------------------------------------------------------------------------

def logout_usuario(request):
    logout(request)
    return render(request, 'acervo_pessoal/login_usuario.html')

#---------------------------------------------------------------------------------------------------------------

@login_required(login_url='/acervo_pessoal/login_usuario/')
def registrar_emprestimo(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    contatos = Contato.objects.all()

    if request.method == 'POST':
        email = request.POST.get('email')
        contato = request.POST.get('contato')
        contato = Contato.objects.get(pk = contato)

        # Salvando o empréstimo diretamente no banco de dados
        emprestimo = Emprestimo.objects.create(livro=livro, contato=contato)
        if emprestimo:
            livro.qtd_total = livro.qtd_total - 1
            livro.livro_emprestado = True
            #muda_status = E
            livro.save()
            messages.success(request, 'Empréstimo registrado com sucesso!')
            return redirect('acervo_pessoal:lista_livros_emprestados')
        else:
            messages.error(request, 'Erro ao registrar empréstimo.')
            return redirect('acervo_pessoal:registrar_emprestimo.html')  # Substitua pelo nome correto da sua URL
    return render(request, 'acervo_pessoal/registrar_emprestimo.html', {'livro': livro,'contatos': contatos})

@login_required(login_url='/acervo_pessoal/login_usuario/')
def lista_livros_emprestados(request):
    livros_emprestados = Livro.objects.filter(livro_emprestado=True)
    total_livros_emprestados = livros_emprestados.count()

    return render(request, 'acervo_pessoal/lista_livros_emprestados.html', {'livros_emprestados': livros_emprestados, 'total_livros_emprestados': total_livros_emprestados})

@login_required(login_url='/acervo_pessoal/login_usuario/')
def registrar_devolucao(request, livro_id):
    emprestimo = get_object_or_404(Emprestimo, pk=livro_id)
    livro = emprestimo.livro
    contatos = Contato.objects.all()  # Pode ser útil para selecionar o contato de devolução

    if request.method == 'POST':
        contato_id = request.POST.get('contato')
        contato_devolucao = Contato.objects.get(pk=contato_id)

        # emprestimo.data_devolucao = timezone.now()
        emprestimo.contato = contato_devolucao
        emprestimo.save()

        livro.qtd_total = livro.qtd_total + 1
        livro.livro_emprestado = False
        livro.save()

        messages.success(request, 'Devolução registrada com sucesso!')
        return redirect('acervo_pessoal:registrar_devolucao', livro.id)

    return render(request, 'acervo_pessoal/registrar_devolucao.html', {'emprestimo': emprestimo, 'contatos': contatos})

#---------------------------------------------------------------------------------------------------------------
def lista_contato():
    pass
@login_required(login_url='/acervo_pessoal/login_usuario/')
def cadastro_contato(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        verifica = True
        # Verifica se o e-mail é único
        if Contato.objects.filter(email=email).exists():
            messages.error(request, 'Contato existente!')
            verifica = False

        # Se todas as verificações passarem, cria um novo contato
        if verifica:
            novo_contato = Contato(nome=nome, telefone=telefone, email=email)
            novo_contato.save()
            messages.success(request, 'Contato registrado com sucesso!')
        else:
            messages.error(request, 'Erro ao criar contato!')

        # Após o cadastro, redireciona para a página desejada
        return redirect('acervo_pessoal:lista_livros_disponiveis')

    # Se o método não for POST, exibe o formulário
    return render(request, 'acervo_pessoal/cadastro_contato.html')

#---------------------------------------------------------------------------------------------------------------
@login_required(login_url='/acervo_pessoal/login_usuario/')
def pesquisar_livro(request):
    termo_pesquisa = request.GET.get('titulo', '')
    livros_encontrados = []

    if termo_pesquisa:
        pesquisa_itens = PesquisaItens()
        livros_encontrados = pesquisa_itens.pesquisa_por_nome(termo_pesquisa)

    return render(request, 'acervo_pessoal/pesquisa.html', {'livros_encontrados': livros_encontrados, 'termo_pesquisa': termo_pesquisa})

    # livros_encontrados = []  # Inicializa com uma lista vazia

    # if request.method == 'GET':
    #     titulo_livro = request.GET.get('titulo', '')  # Obter o título do livro da consulta GET
    #     pesquisa_itens = PesquisaItens()
    #     livros_encontrados = pesquisa_itens.pesquisa_por_nome(titulo_livro)

    #     return render(request, 'acervo_pessoal/resultado_pesquisa.html', {'livros_encontrados': livros_encontrados, 'termo_pesquisa': titulo_livro})

    # return render(request, 'acervo_pessoal/pesquisar_livro.html')


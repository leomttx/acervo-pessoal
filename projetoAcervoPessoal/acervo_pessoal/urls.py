from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "acervo_pessoal"
urlpatterns = [
    #Ex: acervo_pessoal/cad_livro/
    path("cad_livro/", views.cad_livro, name='cad_livro'),
    path("lista_livros_disponiveis/", views.lista_livros_disponiveis, name='lista_livros_disponiveis'),
    path("lista_livros_emprestados/", views.lista_livros_emprestados, name='lista_livros_emprestados'),
    path("registrar_emprestimo/<int:livro_id>/", views.registrar_emprestimo, name='registrar_emprestimo'),
    path("registrar_devolucao/<int:livro_id>/", views.registrar_devolucao, name='registrar_devolucao'),
    path('pesquisar_livro/', views.pesquisar_livro, name='pesquisar_livro'),
    path('cadastro_contato/', views.cadastro_contato, name='cadastro_contato'),
    path('lista_contato/', views.lista_contato, name='lista_contato'),
    path('cad_usuario/', views.cad_usuario, name='cad_usuario'),
    path('login_usuario/', views.login_usuario, name='login_usuario'),
    path('logout_usuario/', views.logout_usuario, name='logout_usuario'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
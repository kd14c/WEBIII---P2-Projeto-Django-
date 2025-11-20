from django.contrib import admin
from .models import Pagina, Produto, Contato, Pedido

@admin.register(Pagina)
class PaginaAdmin(admin.ModelAdmin):
    list_display = ('nome_do_site', 'email', 'whatsapp', 'atualizado_em')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'criado_em')
    search_fields = ('nome',)
    list_filter = ('criado_em',)

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'criado_em')
    search_fields = ('nome', 'email')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'produto', 'quantidade', 'total', 'data')
    list_filter = ('data', 'produto')

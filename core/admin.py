from django.contrib import admin
from django.utils.html import format_html
from .models import Pagina, Produto, Contato, Pedido

@admin.register(Pagina)
class PaginaAdmin(admin.ModelAdmin):
    list_display = ('nome_do_site', 'email', 'whatsapp', 'atualizado_em')


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'nome', 'preco', 'estoque', 'criado_em')
    search_fields = ('nome',)
    list_filter = ('criado_em',)
    ordering = ('-criado_em',)

    def thumb(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="50" style="border-radius:5px;">', obj.foto.url)
        return "—"

    thumb.short_description = "Imagem"


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'criado_em')
    search_fields = ('nome', 'email')
    ordering = ('-criado_em',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario_link', 'produto', 'quantidade', 'total', 'data')
    list_filter = ('data', 'produto')
    readonly_fields = ('total', 'data')
    ordering = ('-data',)

    def usuario_link(self, obj):
        return obj.usuario.username

    usuario_link.short_description = "Usuário"

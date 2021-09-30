from django.contrib import admin
from django.utils.html import format_html


from .models import (
    Autor,
    Genero,
    Livros,
    CadReserva,
    CadAluguel,
)


class AutorAdmin(admin.ModelAdmin):
    fields = ('nome',)
    list_display = ('nome',)
    search_fields = ('nome',)


class GeneroAdmin(admin.ModelAdmin):
    fields = ('genero',)
    list_display = ('genero',)
    search_fields = ('genero',)


class LivrosAdmin(admin.ModelAdmin):
    fields = ('autor', 'genero', 'titulo', 'foto', 'destaque', 'ativo')
    list_filter = ('autor', 'genero', 'titulo', 'destaque', 'ativo')
    list_display = ('id', 'link_titulo', 'autor', 'genero',
                    'data_cadastro', 'destaque', 'ativo')
    search_fields = ('titulo', 'autor', 'genero')

    def link_titulo(self, obj):
        return format_html('<a href="{}">{}</a>'.format(obj.id, obj.titulo))

    link_titulo.allow_tags = True
    link_titulo.short_description = 'Título'
    link_titulo.admin_order_field = 'titulo'


class CadReservaAdmin(admin.ModelAdmin):
    fields = ('livro', 'usuario', 'ativo')
    list_display = ('livro', 'usuario', 'data_cad_reserva', 'ativo')
    list_filter = ('livro', 'usuario', 'data_cad_reserva', 'ativo')
    search_fields = ('livro', 'usuario')


class CadAluguelAdmin(admin.ModelAdmin):
    fields = ('livro', 'usuario', 'ativo', 'devolvido')
    list_display = ('livro', 'usuario', 'data_cad_aluguel',
                    'data_renovacao', 'ativo', 'devolvido')
    list_filter = ('data_cad_aluguel', 'data_renovacao', 'ativo', 'devolvido')
    search_fields = ('livro', 'usuario')


admin.site.register(Livros, LivrosAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(CadReserva, CadReservaAdmin)
admin.site.register(CadAluguel, CadAluguelAdmin)

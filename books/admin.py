from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.views.main import ChangeList
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
    fields = ('autor', 'genero', 'titulo', 'foto',
              'destaque', 'ativo', 'alugado')
    list_filter = ('autor', 'genero', 'titulo', 'destaque', 'ativo', 'alugado')
    list_display = ('id', 'link_titulo', 'autor', 'genero',
                    'data_cadastro', 'destaque', 'ativo', 'alugado')
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
    search_fields = ('livro__titulo', 'usuario__nome')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            parent_id = request.resolver_match.kwargs['object_id']
            if db_field.name == "livro":
                if parent_id:
                    pass
                else:
                    kwargs["queryset"] = Livros.objects.filter(alugado=False)
        except:
            if db_field.name == "livro":
                kwargs["queryset"] = Livros.objects.filter(alugado=False)
            print("erro")
        return super(CadAluguelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_queryset(self, request):
    #     return super(CadAluguelAdmin, self).get_queryset(request).filter(livro__alugado=True)

    def save_model(self, request, obj, form, change):
        book = Livros.objects.get(id=obj.livro.id)
        if obj.ativo:
            book.alugado = True
            book.save()
        else:
            book.alugado = False
            book.save()
        super().save_model(request, obj, form, change)


admin.site.register(Livros, LivrosAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Autor, AutorAdmin)
# admin.site.register(CadReserva, CadReservaAdmin)
admin.site.register(CadAluguel, CadAluguelAdmin)

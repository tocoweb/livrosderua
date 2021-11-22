from accounts.models import User
from django.db import models
from django.db.models.base import Model, ModelStateFieldsCacheDescriptor
from django.db.models.expressions import OrderBy
from django.db.models.fields import DateField


class Autor(models.Model):
    nome = models.CharField(max_length=250)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return self.nome


class Genero(models.Model):
    genero = models.CharField(max_length=250)

    class Meta:
        ordering = ['genero']
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'

    def __str__(self):
        return self.genero


class Livros(models.Model):
    autor = models.ForeignKey(
        Autor, verbose_name='Autor', blank=False, null=False, on_delete=models.CASCADE)
    genero = models.ForeignKey(
        Genero, verbose_name='Gênero', blank=False, null=False, on_delete=models.CASCADE)
    titulo = models.CharField(verbose_name='Título',
                              max_length=350, blank=False, null=False)
    foto = models.ImageField(verbose_name='Foto capa',
                             upload_to='fotos', null=True, blank=True)
    destaque = models.BooleanField(
        verbose_name='Destacar livro?', default=False)
    data_cadastro = models.DateField(
        verbose_name='Data cadastro', auto_now_add=True, auto_now=False)
    ativo = models.BooleanField(default=True)
    alugado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.foto:
            from core.utils import generate_thumbnail_crop

            self.foto = generate_thumbnail_crop(self.foto, 100, 120)
        super(Livros, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-data_cadastro']
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'

    def __str__(self):
        return f'{self.id} - {self.titulo}'


class CadReserva(models.Model):
    livro = models.ForeignKey(
        Livros, verbose_name='Livro', blank=False, null=False, on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        User, verbose_name='Usuário', blank=False, null=False, on_delete=models.CASCADE)
    data_cad_reserva = models.DateField(
        verbose_name='Data cadastro da reserva', auto_now_add=True, auto_now=False)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['data_cad_reserva']
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return self.usuario.nome


class CadAluguel(models.Model):
    livro = models.ForeignKey(
        Livros, verbose_name='Livro', blank=False, null=False, on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        User, verbose_name='Usuário', blank=False, null=False, on_delete=models.CASCADE)
    data_cad_aluguel = models.DateField(
        verbose_name='Data cadastro do aluguel', auto_now_add=True, auto_now=False)
    data_renovacao = models.DateField(
        verbose_name='Data da renovação', auto_now_add=False, auto_now=True)
    ativo = models.BooleanField(default=True)
    devolvido = models.BooleanField(default=False)

    class Meta:
        ordering = ['data_cad_aluguel']
        verbose_name = 'Aluguel'
        verbose_name_plural = 'Alugueis'

    def __str__(self):
        return f'Usuário: {self.usuario.nome} -- Livro: {self.livro}'

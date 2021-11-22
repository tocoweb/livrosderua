from os import name
from django.conf import settings
from books.models import Autor, CadReserva, Livros
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from .forms import EmailForm

from accounts.forms import CadForm


def home(request):
    livros = Livros.objects.filter(ativo=True)
    reservas = CadReserva.objects.filter(ativo=True)

    query = request.GET.get('q')
    if query:
        livros = Livros.objects.filter(
            Q(titulo__icontains=query, ativo=True) | Q(
                autor__nome__icontains=query, ativo=True)
        )
        if livros.count() == 0:
            messages.add_message(request, messages.INFO,
                                 'Nenhum livro encontrado com esses termos.')

    page = request.GET.get('page', 1)

    paginator = Paginator(livros, 25)

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'livros': livros,
        'books': books,
        'reservas': reservas,
    }

    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def contato(request):
    messageSent = False

    # check if form has been submitted
    if request.method == 'POST':

        form = EmailForm(request.POST)

        # check if data from the form is clean
        if form.is_valid():
            subject = "Formulário contato - Livros de Rua"
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            telefone = form.cleaned_data['telefone']
            assunto = form.cleaned_data['assunto']

            message = "Nome: " + nome + " | E-mail: " + email + \
                " | Telefone: " + telefone + " | Assunto: " + assunto

            # send the email to the recipent
            send_mail(subject, message,
                      settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])

            # set the variable initially created to True
            messageSent = True

    else:
        form = EmailForm()

    return render(request, 'contato.html', {'form': form, 'messageSent': messageSent})


def cadastro(request):
    if request.method == 'POST':
        form = CadForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            cpf = form.cleaned_data['cpf']
            telefone = form.cleaned_data['telefone']
            rua = form.cleaned_data['rua']
            numero = form.cleaned_data['numero']
            bairro = form.cleaned_data['bairro']
            cidade = form.cleaned_data['cidade']
            email = form.cleaned_data['email']
            form.save()
            return redirect('/')
    else:
        form = CadForm()
        context = {'form': form}
        return render(request, 'cad-user.html', context)

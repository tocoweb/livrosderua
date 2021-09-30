from books.models import Livros
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.forms import CadForm


def home(request):
    livros = Livros.objects.filter(ativo=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(livros, 9)

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'livros': livros,
        'books': books,
    }

    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def contato(request):
    return render(request, 'contato.html')


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

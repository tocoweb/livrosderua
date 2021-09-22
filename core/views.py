from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contato(request):
    return render(request, 'contato.html')


def cadastro(request):
    return render(request, 'cad-user.html')

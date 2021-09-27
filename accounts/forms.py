from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model


User = get_user_model()


class CadForm(UserCreationForm):
    nome = forms.CharField(max_length=250, required=True)
    cpf = forms.CharField(max_length=15, required=True)
    telefone = forms.CharField(max_length=15, required=True)
    rua = forms.CharField(max_length=250, required=True)
    numero = forms.CharField(max_length=6, required=True)
    bairro = forms.CharField(max_length=250, required=True)
    cidade = forms.CharField(max_length=250, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'nome',
            'cpf',
            'telefone',
            'rua',
            'numero',
            'bairro',
            'cidade',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(CadForm, self).save(commit=False)
        if commit:
            user.save()

        return user

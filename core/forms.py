from django import forms


class EmailForm(forms.Form):
    nome = forms.CharField(label='Nome', required=True)
    email = forms.EmailField(label='E-mail', required=True)
    telefone = forms.CharField(label='Telefone')
    assunto = forms.CharField(widget=forms.Textarea,
                              label='Assunto')
